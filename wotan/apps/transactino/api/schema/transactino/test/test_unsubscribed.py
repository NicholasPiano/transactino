
import json

from django.conf import settings
from django.test import TestCase

from util.find_in_dictionary import find_in_dictionary
from util.extract_schema_paths import extract_schema_paths
from util.gpg import GPG

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants
from apps.subscription.models import (
  Account,
  Announcement,
  Challenge,
  System,
  Connection,
  Subscription,
  Payment,
)
from apps.subscription.models.account.constants import account_fields
from apps.subscription.models.account.schema.unsubscribed.methods.constants import (
  account_unsubscribed_method_constants,
)
from apps.subscription.models.announcement.constants import announcement_fields
from apps.subscription.models.challenge.constants import challenge_fields
from apps.subscription.models.challenge.schema.common.methods.constants import (
  challenge_method_constants,
  respond_constants as challenge_respond_constants,
  get_constants as challenge_get_constants,
)
from apps.subscription.models.system.constants import system_fields
from apps.subscription.models.subscription.constants import subscription_fields
from apps.subscription.models.subscription.schema.common.methods.constants import (
  subscription_method_constants,
  get_constants as subscription_get_constants,
  activate_constants as subscription_activate_constants,
)
from apps.subscription.models.payment.constants import payment_fields
from apps.subscription.models.payment.schema.common.methods.constants import (
  get_constants as payment_get_constants,
)

from ....constants import api_constants
from ..constants import transactino_constants
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

  def test_schema_paths(self):
    null_payload = None

    response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=null_payload,
    )
    rendered_response = response.render()
    paths = extract_schema_paths(rendered_response)

    self.assertEqual(
      paths,
      [
        [
          api_constants.SCHEMA,
          transactino_constants.README,
        ],
        [
          api_constants.SCHEMA,
          transactino_constants.SOCKET,
        ],
        [
          api_constants.SCHEMA,
          transactino_constants.SYSTEM,
        ],
        [
          api_constants.SCHEMA,
          transactino_constants.ANNOUNCEMENTS,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Account.__name__,
          schema_constants.METHODS,
          account_unsubscribed_method_constants.VERIFY,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Account.__name__,
          schema_constants.METHODS,
          method_constants.DELETE,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Announcement.__name__,
          schema_constants.METHODS,
          method_constants.GET,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Announcement.__name__,
          schema_constants.INSTANCES,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          challenge_method_constants.RESPOND,
          challenge_respond_constants.CHALLENGE_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          challenge_method_constants.RESPOND,
          challenge_respond_constants.CONTENT,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          challenge_get_constants.CHALLENGE_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          challenge_fields.IS_OPEN,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.INSTANCES,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          System.__name__,
          schema_constants.METHODS,
          method_constants.GET,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          System.__name__,
          schema_constants.INSTANCES,
        ],
      ],
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

    self.assertTrue(Account.objects.get(public_key=self.public_key).is_verified)

  def test_account_delete(self):
    delete_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Account.__name__: {
            schema_constants.METHODS: {
              method_constants.DELETE: {},
            },
          },
        },
      },
    }

    delete_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=delete_payload,
    )

    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    imported_key = gpg.import_key(settings.TEST_PRIVATE_KEY)
    imported_system_key = gpg.import_key(settings.TEST_SYSTEM_PRIVATE_KEY)
    challenge = self.account.challenges.get()

    encrypted_content = find_in_dictionary(
      delete_response.render(),
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
    second_delete_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=delete_payload,
    )

    self.assertFalse(Account.objects.get(public_key=self.public_key))

  def test_announcement_get(self):
    active_announcement = Announcement.objects.create_and_sign(
      system=self.system,
      matter='active',
    )
    active_announcement.activate()
    inactive_announcement = Announcement.objects.create_and_sign(
      system=self.system,
      matter='inactive',
    )

    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Announcement.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {},
            },
          },
        },
      },
    }

    get_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=get_payload,
    )

    paths = extract_schema_paths(get_response.render(), null=False)

    self.assertEqual(
      paths,
      [
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Announcement.__name__,
          schema_constants.METHODS,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Announcement.__name__,
          schema_constants.INSTANCES,
          active_announcement._id,
          schema_constants.ATTRIBUTES,
          announcement_fields.MATTER,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Announcement.__name__,
          schema_constants.INSTANCES,
          active_announcement._id,
          schema_constants.ATTRIBUTES,
          announcement_fields.SIGNATURE,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Announcement.__name__,
          schema_constants.INSTANCES,
          active_announcement._id,
          schema_constants.ATTRIBUTES,
          announcement_fields.DATE_ACTIVATED,
        ],
      ],
    )

  def test_announcement_notification(self):
    active_announcement = Announcement.objects.create_and_sign(
      system=self.system,
      matter='active',
    )
    active_announcement.activate()

    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Challenge.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {},
            },
          },
        },
      },
    }

    get_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=get_payload,
    )

    schema_response = get_response.get_child(api_constants.SCHEMA)
    announcements_response = schema_response.get_child(transactino_constants.ANNOUNCEMENTS)

    self.assertTrue(announcements_response)

  def test_challenge_get(self):
    open_challenge_content = 'open_challenge_content'
    open_challenge = self.account.challenges.create(
      is_open=True,
      encrypted_content=open_challenge_content,
    )
    closed_challenge_content = 'closed_challenge_content'
    closed_challenge = self.account.challenges.create(
      is_open=False,
      encrypted_content=closed_challenge_content,
    )

    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Challenge.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {},
            },
          },
        },
      },
    }

    get_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=get_payload,
    )

    paths = extract_schema_paths(get_response.render(), null=False)

    self.assertEqual(
      paths,
      [
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          challenge_get_constants.CHALLENGE_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          challenge_fields.IS_OPEN,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.INSTANCES,
          open_challenge._id,
          schema_constants.ATTRIBUTES,
          challenge_fields.ENCRYPTED_CONTENT,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.INSTANCES,
          closed_challenge._id,
          schema_constants.ATTRIBUTES,
          challenge_fields.ENCRYPTED_CONTENT,
        ],
      ],
    )

  def test_system_get(self):
    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          System.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {},
            },
          },
        },
      },
    }

    get_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=get_payload,
    )

    paths = extract_schema_paths(get_response.render(), null=False)

    self.assertEqual(
      paths,
      [
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          System.__name__,
          schema_constants.METHODS,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          System.__name__,
          schema_constants.INSTANCES,
          self.system._id,
          schema_constants.ATTRIBUTES,
          system_fields.PUBLIC_KEY,
        ],
      ],
    )

class UnsubscribedAccountVerifiedTestCase(TestCase):
  def setUp(self):
    self.schema = TransactinoSchema()
    self.system = System.objects.create_and_import(
      public_key=settings.TEST_SYSTEM_PUBLIC_KEY,
      private_key=settings.TEST_SYSTEM_PRIVATE_KEY,
    )
    self.public_key = settings.TEST_PUBLIC_KEY
    self.ip_value = 'ip_value'
    self.channel_name = 'channel_name'
    self.account = Account.objects.create(public_key=self.public_key, is_verified=True)
    self.account.import_public_key()
    self.ip = self.account.ips.create(value=self.ip_value)
    self.connection, connection_created = Connection.objects.bring_online(
      name=self.channel_name,
      ip_value=self.ip_value,
    )

  def test_schema_paths(self):
    null_payload = None

    response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=null_payload,
    )
    rendered_response = response.render()
    paths = extract_schema_paths(rendered_response)

    self.assertEqual(
      paths,
      [
        [
          api_constants.SCHEMA,
          transactino_constants.README,
        ],
        [
          api_constants.SCHEMA,
          transactino_constants.SOCKET,
        ],
        [
          api_constants.SCHEMA,
          transactino_constants.SYSTEM,
        ],
        [
          api_constants.SCHEMA,
          transactino_constants.ANNOUNCEMENTS,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Account.__name__,
          schema_constants.METHODS,
          account_unsubscribed_method_constants.VERIFY,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Account.__name__,
          schema_constants.METHODS,
          method_constants.DELETE,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Announcement.__name__,
          schema_constants.METHODS,
          method_constants.GET,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Announcement.__name__,
          schema_constants.INSTANCES,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          challenge_method_constants.RESPOND,
          challenge_respond_constants.CHALLENGE_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          challenge_method_constants.RESPOND,
          challenge_respond_constants.CONTENT,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          challenge_get_constants.CHALLENGE_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          challenge_fields.IS_OPEN,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Challenge.__name__,
          schema_constants.INSTANCES,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          System.__name__,
          schema_constants.METHODS,
          method_constants.GET,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          System.__name__,
          schema_constants.INSTANCES,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.METHODS,
          method_constants.CREATE,
          subscription_fields.DURATION_IN_DAYS,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.METHODS,
          method_constants.CREATE,
          subscription_fields.ACTIVATION_DATE,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.METHODS,
          subscription_method_constants.ACTIVATE,
          subscription_activate_constants.SUBSCRIPTION_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          subscription_get_constants.SUBSCRIPTION_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          subscription_fields.IS_ACTIVE,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.INSTANCES,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          payment_get_constants.PAYMENT_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          payment_fields.IS_OPEN,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.INSTANCES,
        ],
      ],
    )

  def test_subscription_get(self):
    subscription = self.account.subscriptions.create(is_active=False)
    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Subscription.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {},
            },
          },
        },
      },
    }

    get_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=get_payload,
    )

    paths = extract_schema_paths(get_response.render(), null=False)

    self.assertEqual(
      paths,
      [
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          subscription_get_constants.SUBSCRIPTION_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          subscription_fields.IS_ACTIVE,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.INSTANCES,
          subscription._id,
          schema_constants.ATTRIBUTES,
          subscription_fields.ORIGIN,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.INSTANCES,
          subscription._id,
          schema_constants.ATTRIBUTES,
          subscription_fields.DURATION_IN_DAYS,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.INSTANCES,
          subscription._id,
          schema_constants.ATTRIBUTES,
          subscription_fields.ACTIVATION_DATE,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.INSTANCES,
          subscription._id,
          schema_constants.ATTRIBUTES,
          subscription_fields.IS_VALID_UNTIL,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.INSTANCES,
          subscription._id,
          schema_constants.ATTRIBUTES,
          subscription_fields.HAS_BEEN_ACTIVATED,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Subscription.__name__,
          schema_constants.INSTANCES,
          subscription._id,
          schema_constants.ATTRIBUTES,
          subscription_fields.IS_ACTIVE,
        ],
      ],
    )

  def test_payment_get(self):
    payment = self.account.payments.create(is_open=True)
    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Payment.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {},
            },
          },
        },
      },
    }

    get_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=get_payload,
    )

    print(json.dumps(get_response.render(), indent=2))

    paths = extract_schema_paths(get_response.render(), null=False)

    self.assertEqual(
      paths,
      [
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          payment_get_constants.PAYMENT_ID,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.METHODS,
          method_constants.GET,
          payment_fields.IS_OPEN,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.INSTANCES,
          payment._id,
          schema_constants.ATTRIBUTES,
          payment_fields.ORIGIN,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.INSTANCES,
          payment._id,
          schema_constants.ATTRIBUTES,
          payment_fields.IS_OPEN,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.INSTANCES,
          payment._id,
          schema_constants.ATTRIBUTES,
          payment_fields.TIME_CONFIRMED,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.INSTANCES,
          payment._id,
          schema_constants.ATTRIBUTES,
          payment_fields.FULL_BTC_AMOUNT,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.INSTANCES,
          payment._id,
          schema_constants.ATTRIBUTES,
          payment_fields.BLOCK_HASH,
        ],
        [
          api_constants.SCHEMA,
          api_constants.MODELS,
          Payment.__name__,
          schema_constants.INSTANCES,
          payment._id,
          schema_constants.ATTRIBUTES,
          payment_fields.TXID,
        ],
      ],
    )
