
import json

from django.conf import settings
from django.test import TestCase

from util.find_in_dictionary import find_in_dictionary
from util.gpg import GPG

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants
from apps.subscription.models import (
  Account,
  Challenge,
  System,
  Connection,
)
from apps.subscription.models.account.constants import account_fields
from apps.subscription.models.account.schema.unsubscribed.methods.constants import (
  account_unsubscribed_method_constants,
)
from apps.subscription.models.challenge.constants import challenge_fields
from apps.subscription.models.challenge.schema.common.methods.constants import (
  challenge_method_constants,
  respond_constants as challenge_respond_constants,
)

from ....constants import api_constants
from .. import TransactinoSchema

class UnsubscribedAccountNotVerifiedTestCase(TestCase):
  def setUp(self):
    self.schema = TransactinoSchema()
    self.system = System.objects.create_and_import(
      public_key=settings.TEST_SYSTEM_PUBLIC_KEY,
      private_key=settings.TEST_SYSTEM_PRIVATE_KEY,
    )
    self.public_key = settings.TEST_PUBLIC_KEY
    self.ip_value = 'ip_value'
    self.channel_name = 'channel_name'
    self.account = Account.objects.create(public_key=self.public_key)
    self.account.import_public_key()
    self.ip = self.account.ips.create(value=self.ip_value)
    self.connection, connection_created = Connection.objects.bring_online(
      name=self.channel_name,
      ip_value=self.ip_value,
    )

  def test_account_verify(self):
    verify_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Account.__name__: {
            schema_constants.METHODS: {
              account_unsubscribed_method_constants.VERIFY: {},
            },
          },
        },
      },
    }

    verify_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=verify_payload,
    )

    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    imported_key = gpg.import_key(settings.TEST_PRIVATE_KEY)
    imported_system_key = gpg.import_key(settings.TEST_SYSTEM_PRIVATE_KEY)
    challenge = self.account.challenges.get()

    encrypted_content = find_in_dictionary(
      verify_response.render(),
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Challenge.__name__,
        schema_constants.INSTANCES,
        challenge._id,
        schema_constants.ATTRIBUTES,
        challenge_fields.ENCRYPTED_CONTENT,
      ],
    )

    decrypted_content = gpg.decrypt_from_private(encrypted_content)
    reencrypted_content = gpg.encrypt_to_public_with_long_key_id(
      decrypted_content,
      imported_system_key.long_key_id,
    )

    respond_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Challenge.__name__: {
            schema_constants.METHODS: {
              challenge_method_constants.RESPOND: {
                challenge_respond_constants.CHALLENGE_ID: challenge._id,
                challenge_respond_constants.CONTENT: reencrypted_content,
              },
            },
          },
        },
      },
    }

    respond_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=respond_payload,
    )
    second_verify_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=verify_payload,
    )

    self.account.refresh_from_db()

    self.assertTrue(self.account.is_verified)
