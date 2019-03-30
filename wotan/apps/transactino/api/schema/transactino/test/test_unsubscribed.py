
import json

from django.conf import settings
from django.test import TestCase

from util.find_in_dictionary import find_in_dictionary
from util.extract_schema_paths import extract_schema_paths
from util.gpg import GPG

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants
from apps.subscription.models import System, Connection, Account, Challenge
from apps.subscription.models.account.constants import account_fields
from apps.subscription.models.account.schema.unsubscribed.methods.constants import (
  account_unsubscribed_method_constants,
)
from apps.subscription.models.challenge.constants import challenge_fields
from apps.subscription.models.challenge.schema.common.methods.constants import (
  respond_constants,
  challenge_method_constants,
)

from ..constants import transactino_constants
from .. import TransactinoSchema

class UnsubscribedAccountNotVerifiedTestCase(TestCase):
  def setUp(self):
    self.schema = TransactinoSchema()
    self.system = System.objects.create(public_key=settings.TEST_SYSTEM_PUBLIC_KEY)
    self.system.import_public_key()
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

  def test_schema_paths(self):
    null_payload = None

    response = self.schema.respond(payload=null_payload, connection=self.connection)
    rendered_response = response.render()
    paths = extract_schema_paths(rendered_response)

    print(json.dumps(rendered_response, indent=2))

    self.assertTrue(False)
    self.assertEqual(
      paths,
      [
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          Account.__name__,
          schema_constants.METHODS,
          account_unsubscribed_method_constants.VERIFY,
        ],
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          Account.__name__,
          schema_constants.METHODS,
          method_constants.DELETE,
        ],
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          challenge_method_constants.RESPOND,
          respond_constants.CHALLENGE_ID,
        ],
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          challenge_method_constants.RESPOND,
          respond_constants.CONTENT,
        ],
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          challenge_fields.IS_OPEN,
        ],
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          Challenge.__name__,
          schema_constants.INSTANCES,
        ],
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          System.__name__,
          schema_constants.METHODS,
          method_constants.GET,
        ],
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          System.__name__,
          schema_constants.INSTANCES,
        ],
      ],
    )

  # def test_account_verify(self):
  #   verify_payload = {
  #     transactino_constants.SCHEMA: {
  #       transactino_constants.MODELS: {
  #         Account.__name__: {
  #           schema_constants.METHODS: {
  #             account_unsubscribed_method_constants.VERIFY: {},
  #           },
  #         },
  #       },
  #     },
  #   }
  #
  #   verify_response = self.schema.respond(
  #     payload=verify_payload,
  #     connection=self.connection,
  #   )
  #
  #   gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
  #   imported_key = gpg.import_key(settings.TEST_PRIVATE_KEY)
  #   imported_system_key = gpg.import_key(settings.TEST_SYSTEM_PRIVATE_KEY)
  #   challenge = self.account.challenges.get()
  #
  #   encrypted_content = find_in_dictionary(
  #     verify_response.render(),
  #     [
  #       transactino_constants.SCHEMA,
  #       transactino_constants.MODELS,
  #       Challenge.__name__,
  #       schema_constants.INSTANCES,
  #       challenge._id,
  #       schema_constants.ATTRIBUTES,
  #       challenge_fields.ENCRYPTED_CONTENT,
  #     ],
  #   )
  #
  #   decrypted_content = gpg.decrypt_from_private(encrypted_content)
  #   reencrypted_content = gpg.encrypt_to_public_with_long_key_id(
  #     decrypted_content,
  #     imported_system_key.long_key_id,
  #   )
  #
  #   respond_payload = {
  #     transactino_constants.SCHEMA: {
  #       transactino_constants.MODELS: {
  #         Challenge.__name__: {
  #           schema_constants.METHODS: {
  #             challenge_method_constants.RESPOND: {
  #               respond_constants.CHALLENGE_ID: challenge._id,
  #               respond_constants.CONTENT: reencrypted_content,
  #             },
  #           },
  #         },
  #       },
  #     },
  #   }
  #
  #   respond_response = self.schema.respond(
  #     payload=respond_payload,
  #     connection=self.connection,
  #   )
  #   second_verify_response = self.schema.respond(
  #     payload=verify_payload,
  #     connection=self.connection,
  #   )
  #
  #   self.assertTrue(False)
  #   self.assertTrue(Account.objects.get(public_key=self.public_key).is_verified)

  def test_account_delete(self):
    delete_payload = {
      transactino_constants.SCHEMA: {
        transactino_constants.MODELS: {
          Account.__name__: {
            schema_constants.METHODS: {
              method_constants.DELETE: {},
            },
          },
        },
      },
    }

    delete_response = self.schema.respond(
      payload=delete_payload,
      connection=self.connection,
    )

    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    imported_key = gpg.import_key(settings.TEST_PRIVATE_KEY)
    imported_system_key = gpg.import_key(settings.TEST_SYSTEM_PRIVATE_KEY)
    challenge = self.account.challenges.get()

    encrypted_content = find_in_dictionary(
      delete_response.render(),
      [
        transactino_constants.SCHEMA,
        transactino_constants.MODELS,
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
      transactino_constants.SCHEMA: {
        transactino_constants.MODELS: {
          Challenge.__name__: {
            schema_constants.METHODS: {
              challenge_method_constants.RESPOND: {
                respond_constants.CHALLENGE_ID: challenge._id,
                respond_constants.CONTENT: reencrypted_content,
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
    second_delete_response = self.schema.respond(
      payload=delete_payload,
      connection=self.connection,
    )

    self.assertTrue(False)
    self.assertFalse(Account.objects.get(public_key=self.public_key))

  # def test_challenge_get(self):
  #   open_challenge_content = 'open_challenge_content'
  #   open_challenge = self.account.challenges.create(
  #     is_open=True,
  #     encrypted_content=open_challenge_content,
  #   )
  #   closed_challenge_content = 'closed_challenge_content'
  #   closed_challenge = self.account.challenges.create(
  #     is_open=False,
  #     encrypted_content=closed_challenge_content,
  #   )
  #
  #   get_payload = {
  #     transactino_constants.SCHEMA: {
  #       transactino_constants.MODELS: {
  #         Challenge.__name__: {
  #           schema_constants.METHODS: {
  #             method_constants.GET: {},
  #           },
  #         },
  #       },
  #     },
  #   }
  #
  #   get_response = self.schema.respond(
  #     payload=get_payload,
  #     connection=self.connection,
  #   )
  #
  #   paths = extract_schema_paths(get_response.render(), null=False)
  #
  #   self.assertTrue(False)
  #   self.assertEqual(
  #     paths,
  #     [
  #       [
  #         transactino_constants.SCHEMA,
  #         transactino_constants.MODELS,
  #         Challenge.__name__,
  #         schema_constants.METHODS,
  #         method_constants.GET,
  #         challenge_fields.IS_OPEN,
  #       ],
  #       [
  #         transactino_constants.SCHEMA,
  #         transactino_constants.MODELS,
  #         Challenge.__name__,
  #         schema_constants.INSTANCES,
  #         open_challenge._id,
  #         schema_constants.ATTRIBUTES,
  #         challenge_fields.ENCRYPTED_CONTENT,
  #       ],
  #       [
  #         transactino_constants.SCHEMA,
  #         transactino_constants.MODELS,
  #         Challenge.__name__,
  #         schema_constants.INSTANCES,
  #         closed_challenge._id,
  #         schema_constants.ATTRIBUTES,
  #         challenge_fields.ENCRYPTED_CONTENT,
  #       ],
  #     ],
  #   )
  #
  # def test_challenge_get_open(self):
  #   open_challenge_content = 'open_challenge_content'
  #   open_challenge = self.account.challenges.create(
  #     is_open=True,
  #     encrypted_content=open_challenge_content,
  #   )
  #   closed_challenge_content = 'closed_challenge_content'
  #   closed_challenge = self.account.challenges.create(
  #     is_open=False,
  #     encrypted_content=closed_challenge_content,
  #   )
  #
  #   get_payload = {
  #     transactino_constants.SCHEMA: {
  #       transactino_constants.MODELS: {
  #         Challenge.__name__: {
  #           schema_constants.METHODS: {
  #             method_constants.GET: {
  #               challenge_fields.IS_OPEN: True,
  #             },
  #           },
  #         },
  #       },
  #     },
  #   }
  #
  #   get_response = self.schema.respond(
  #     payload=get_payload,
  #     connection=self.connection,
  #   )
  #
  #   rendered_response = get_response.render()
  #   instances = find_in_dictionary(
  #     rendered_response,
  #     [
  #       transactino_constants.SCHEMA,
  #       transactino_constants.MODELS,
  #       Challenge.__name__,
  #       schema_constants.INSTANCES,
  #     ],
  #   )
  #
  #   self.assertTrue(False)
  #   self.assertTrue(open_challenge._id in instances)
  #   self.assertFalse(closed_challenge._id in instances)

class UnsubscribedAccountVerifiedTestCase(TestCase):
  pass
