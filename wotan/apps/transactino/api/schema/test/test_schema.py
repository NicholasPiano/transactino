
import json

from django.conf import settings
from django.db import models
from django.test import TestCase
from django.utils import timezone

from util.gpg import GPG

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants
from apps.subscription.models import Account, IP, Challenge, Subscription, Connection
from apps.subscription.models.account.constants import account_fields
from apps.subscription.models.account.schema.unsubscribed.methods.constants import (
  account_unsubscribed_method_constants,
  verify_constants,
)
from apps.subscription.models.challenge.constants import challenge_fields
from apps.subscription.models.challenge.schema.common.methods.constants import (
  challenge_method_constants,
  respond_constants,
)
from apps.subscription.models.subscription.constants import subscription_fields

from ...constants import api_constants
from .. import TransactinoSchema

class TransactinoSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = TransactinoSchema()
    self.public_key = settings.TEST_PUBLIC_KEY
    self.ip_value = 'ip_value'
    self.channel_name = 'channel_name'
    self.connection = Connection.objects.bring_online(
      name=self.channel_name,
      ip_value=self.ip_value,
      port=0,
    )

  def test_account_verification(self):
    ip_value = 'ip_value'

    create_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Account.__name__: {
            schema_constants.METHODS: {
              method_constants.CREATE: {
                account_fields.PUBLIC_KEY: self.public_key,
              },
            },
          },
        },
      },
    }

    create_response = self.schema.respond(
      payload=create_payload,
      connection=self.connection,
    )

    self.assertTrue(Account.objects.filter(public_key=self.public_key))

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
      payload=verify_payload,
      connection=self.connection,
    )

    ### Simulate user action
    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    imported_key = gpg.import_key(settings.TEST_PRIVATE_KEY)

    challenge_id = list(
      verify_response.render().get(
        api_constants.SCHEMA
      ).get(
        api_constants.MODELS
      ).get(
        Challenge.__name__
      ).get(
        schema_constants.INSTANCES
      ).keys()
    )[0]
    encrypted_message = verify_response.render().get(
      api_constants.SCHEMA
    ).get(
      api_constants.MODELS
    ).get(
      Challenge.__name__
    ).get(
      schema_constants.INSTANCES
    ).get(
      challenge_id
    ).get(
      schema_constants.ATTRIBUTES
    ).get(
      challenge_fields.ENCRYPTED_CONTENT
    )

    decrypted_message = gpg.decrypt_from_private(encrypted_message)

    respond_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Challenge.__name__: {
            schema_constants.METHODS: {
              challenge_method_constants.RESPOND: {
                respond_constants.CHALLENGE_ID: challenge_id,
                respond_constants.PLAINTEXT: decrypted_message,
              },
            },
          },
        },
      },
    }

    respond_response = self.schema.respond(
      payload=respond_payload,
      connection=self.connection,
    )
    second_verify_response = self.schema.respond(
      payload=verify_payload,
      connection=self.connection,
    )

    self.assertTrue(Account.objects.get().is_verified)

  def test_subscription_creation(self):
    create_account_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Account.__name__: {
            schema_constants.METHODS: {
              method_constants.CREATE: {
                account_fields.PUBLIC_KEY: self.public_key,
              },
            },
          },
        },
      },
    }

    create_account_response = self.schema.respond(
      payload=create_account_payload,
      connection=self.connection,
    )

    account = Account.objects.get(public_key=self.public_key)
    self.connection.ip = account.ips.get()

    self.assertTrue(account)

    account.is_verified = True
    account.save()

    create_subscription_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Subscription.__name__: {
            schema_constants.METHODS: {
              method_constants.CREATE: {
                subscription_fields.DURATION_IN_DAYS: 365,
                subscription_fields.ACTIVATION_DATE: str(timezone.now()),
              },
            },
          },
        },
      },
    }

    create_response = self.schema.respond(
      payload=create_subscription_payload,
      connection=self.connection,
    )

    # Simulate user action
    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    imported_key = gpg.import_key(settings.TEST_PRIVATE_KEY)

    challenge_id = list(
      create_response.render().get(
        api_constants.SCHEMA
      ).get(
        api_constants.MODELS
      ).get(
        Challenge.__name__
      ).get(
        schema_constants.INSTANCES
      ).keys()
    )[0]
    encrypted_message = create_response.render().get(
      api_constants.SCHEMA
    ).get(
      api_constants.MODELS
    ).get(
      Challenge.__name__
    ).get(
      schema_constants.INSTANCES
    ).get(
      challenge_id
    ).get(
      schema_constants.ATTRIBUTES
    ).get(
      challenge_fields.ENCRYPTED_CONTENT
    )

    decrypted_message = gpg.decrypt_from_private(encrypted_message)

    respond_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Challenge.__name__: {
            schema_constants.METHODS: {
              challenge_method_constants.RESPOND: {
                respond_constants.CHALLENGE_ID: challenge_id,
                respond_constants.PLAINTEXT: decrypted_message,
              },
            },
          },
        },
      },
    }

    respond_response = self.schema.respond(
      payload=respond_payload,
      connection=self.connection,
    )
    second_create_response = self.schema.respond(
      payload=create_subscription_payload,
      connection=self.connection,
    )

    self.assertTrue(Subscription.objects.filter(account=Account.objects.get()))
