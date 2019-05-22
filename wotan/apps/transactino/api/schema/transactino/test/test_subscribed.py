
import json
from dateutil.parser import parse as parse_datetime

from django.conf import settings
from django.test import TestCase

from util.find_in_dictionary import find_in_dictionary
from util.extract_schema_paths import extract_schema_paths
from util.gpg import GPG

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants
from apps.subscription.models import (
  Account,
  Address,
  Announcement,
  Challenge,
  System,
  Connection,
  Subscription,
  Payment,
  IP,
)
from apps.subscription.models.account.constants import account_fields
from apps.subscription.models.account.schema.subscribed.methods.constants import (
  account_subscribed_method_constants,
  lock_constants as account_lock_constants,
)
from apps.subscription.models.address.constants import address_fields
from apps.subscription.models.address.schema.common.methods.constants import (
  get_constants as address_get_constants,
)
from apps.subscription.models.announcement.constants import announcement_fields
from apps.subscription.models.challenge.constants import challenge_fields
from apps.subscription.models.challenge.schema.common.methods.constants import (
  challenge_method_constants,
  respond_constants as challenge_respond_constants,
  get_constants as challenge_get_constants,
  delete_constants as challenge_delete_constants,
)
from apps.subscription.models.system.constants import system_fields
from apps.subscription.models.subscription.constants import subscription_fields
from apps.subscription.models.subscription.schema.common.methods.constants import (
  subscription_method_constants,
  get_constants as subscription_get_constants,
  activate_constants as subscription_activate_constants,
  create_constants as subscription_create_constants,
)
from apps.subscription.models.payment.constants import payment_fields
from apps.subscription.models.payment.schema.common.methods.constants import (
  get_constants as payment_get_constants,
)
from apps.subscription.models.ip.constants import ip_fields
from apps.subscription.models.ip.schema.subscribed.methods.constants import (
  delete_constants as ip_delete_constants,
  get_constants as ip_get_constants,
  create_constants as ip_create_constants,
)
from apps.subscription.schema.with_challenge.constants import with_challenge_constants
from apps.subscription.schema.with_payment.constants import with_payment_constants

from .....models import (
  FeeReport,
  TransactionReport,
  TransactionMatch,
)
from .....models.fee_report.constants import fee_report_fields
from .....models.fee_report.schema.subscribed.methods.constants import (
  fee_report_subscribed_method_constants,
  delete_constants as fee_report_delete_constants,
  get_constants as fee_report_get_constants,
  activate_constants as fee_report_activate_constants,
  create_constants as fee_report_create_constants,
)
from .....models.transaction_report.constants import transaction_report_fields
from .....models.transaction_report.schema.subscribed.methods.constants import (
  transaction_report_subscribed_method_constants,
  delete_constants as transaction_report_delete_constants,
  get_constants as transaction_report_get_constants,
  activate_constants as transaction_report_activate_constants,
  create_constants as transaction_report_create_constants,
)
from .....models.transaction_report.transaction_match.constants import transaction_match_fields
from .....models.transaction_report.transaction_match.schema.subscribed.methods.constants import (
  transaction_match_subscribed_method_constants,
  get_constants as transaction_match_get_constants,
)
from ....constants import api_constants
from ..constants import transactino_constants
from .. import TransactinoSchema

class SubscribedTestCase(TestCase):
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
    self.subscription = self.account.subscriptions.create(is_active=True)
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

    expected_paths = [
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
        account_subscribed_method_constants.LOCK,
        account_lock_constants.LOCK,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Address.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        address_get_constants.ADDRESS_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Address.__name__,
        schema_constants.INSTANCES,
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
        schema_constants.METHODS,
        method_constants.DELETE,
        challenge_delete_constants.CHALLENGE_ID,
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
        IP.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        ip_fields.VALUE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        IP.__name__,
        schema_constants.METHODS,
        method_constants.DELETE,
        ip_delete_constants.IP_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        IP.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        ip_get_constants.IP_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        IP.__name__,
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
        FeeReport.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        fee_report_fields.BLOCKS_TO_INCLUDE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        fee_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.METHODS,
        method_constants.DELETE,
        fee_report_delete_constants.FEE_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        fee_report_get_constants.FEE_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        fee_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.METHODS,
        fee_report_subscribed_method_constants.ACTIVATE,
        fee_report_activate_constants.FEE_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.METHODS,
        fee_report_subscribed_method_constants.ACTIVATE,
        fee_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.INSTANCES,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        transaction_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        transaction_report_fields.TARGET_ADDRESS,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        transaction_report_fields.VALUE_EQUAL_TO,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        transaction_report_fields.VALUE_LESS_THAN,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        transaction_report_fields.VALUE_GREATER_THAN,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.DELETE,
        transaction_report_delete_constants.TRANSACTION_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_report_get_constants.TRANSACTION_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        transaction_report_subscribed_method_constants.ACTIVATE,
        transaction_report_activate_constants.TRANSACTION_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        transaction_report_subscribed_method_constants.ACTIVATE,
        transaction_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.INSTANCES,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_get_constants.TRANSACTION_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_get_constants.TRANSACTION_REPORT_TARGET_ADDRESS,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_get_constants.TRANSACTION_REPORT_IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_get_constants.TRANSACTION_MATCH_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_fields.IS_NEW,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_fields.BLOCK_HASH,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        transaction_match_subscribed_method_constants.DISMISS,
        transaction_match_get_constants.TRANSACTION_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        transaction_match_subscribed_method_constants.DISMISS,
        transaction_match_get_constants.TRANSACTION_REPORT_TARGET_ADDRESS,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        transaction_match_subscribed_method_constants.DISMISS,
        transaction_match_get_constants.TRANSACTION_REPORT_IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        transaction_match_subscribed_method_constants.DISMISS,
        transaction_match_get_constants.TRANSACTION_MATCH_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        transaction_match_subscribed_method_constants.DISMISS,
        transaction_match_fields.BLOCK_HASH,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.INSTANCES,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_account_lock(self):
    self.account.challenges.create(origin=account_lock_constants.ORIGIN, is_open=False, has_been_used=False)
    lock_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Account.__name__: {
            schema_constants.METHODS: {
              account_subscribed_method_constants.LOCK: {
                account_lock_constants.LOCK: True,
              },
            },
          },
        },
      },
    }

    lock_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=lock_payload,
    )

    self.account.refresh_from_db()

    self.assertTrue(self.account.is_locked)

  def test_address_get(self):
    active_address = Address.objects.create(value='active_address')
    inactive_address = Address.objects.create(
      value='inactive_address',
      is_active=False,
    )

    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Address.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {
                address_get_constants.ADDRESS_ID: active_address._id,
              },
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

    expected_paths = [
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Address.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        address_get_constants.ADDRESS_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Address.__name__,
        schema_constants.INSTANCES,
        active_address._id,
        schema_constants.ATTRIBUTES,
        address_fields.VALUE,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

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

    expected_paths = [
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
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

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

    expected_paths = [
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
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        System.__name__,
        schema_constants.INSTANCES,
        self.system._id,
        schema_constants.ATTRIBUTES,
        system_fields.GUARANTEE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        System.__name__,
        schema_constants.INSTANCES,
        self.system._id,
        schema_constants.ATTRIBUTES,
        system_fields.GUARANTEE_SIGNATURE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        System.__name__,
        schema_constants.INSTANCES,
        self.system._id,
        schema_constants.ATTRIBUTES,
        system_fields.DISCLAIMER,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        System.__name__,
        schema_constants.INSTANCES,
        self.system._id,
        schema_constants.ATTRIBUTES,
        system_fields.DISCLAIMER_SIGNATURE,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

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

    expected_paths = [
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
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_ip_create(self):
    self.account.challenges.create(origin=ip_create_constants.ORIGIN, is_open=False, has_been_used=False)

    ip_value = '255.255.255.255'

    create_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          IP.__name__: {
            schema_constants.METHODS: {
              method_constants.CREATE: {
                ip_fields.VALUE: ip_value,
              },
            },
          },
        },
      },
    }

    create_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=create_payload,
    )

    ip = self.account.ips.get(value=ip_value)

    self.assertTrue(ip is not None)

  def test_ip_create_beyond_max(self):
    for _ in range(ip_create_constants.MAX_IPS):
      self.account.ips.create(value='value')

    self.account.payments.create(origin=ip_create_constants.ORIGIN, is_open=False, has_been_used=False)
    self.account.challenges.create(origin=ip_create_constants.ORIGIN, is_open=False, has_been_used=False)

    ip_value = '255.255.255.255'

    create_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          IP.__name__: {
            schema_constants.METHODS: {
              method_constants.CREATE: {
                ip_fields.VALUE: ip_value,
              },
            },
          },
        },
      },
    }

    create_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=create_payload,
    )

    ip = self.account.ips.get(value=ip_value)

    paths = extract_schema_paths(create_response.render(), null=False)

    expected_paths = [
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        IP.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        with_challenge_constants.CHALLENGE_COMPLETE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        IP.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        with_payment_constants.PAYMENT_COMPLETE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        IP.__name__,
        schema_constants.INSTANCES,
        ip._id,
        schema_constants.ATTRIBUTES,
        ip_fields.VALUE,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_ip_delete(self):
    ip_value = '255.255.255.255'

    ip = self.account.ips.create(value=ip_value)

    self.account.challenges.create(origin=ip_delete_constants.ORIGIN, is_open=False, has_been_used=False)

    delete_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          IP.__name__: {
            schema_constants.METHODS: {
              method_constants.DELETE: {
                ip_delete_constants.IP_ID: ip._id,
              },
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

    self.assertFalse(self.account.ips.filter(value=ip_value).exists())

  def test_ip_get(self):
    self.account.challenges.create(origin=ip_get_constants.ORIGIN, is_open=False, has_been_used=False)
    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          IP.__name__: {
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

    expected_paths = [
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        IP.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        with_challenge_constants.CHALLENGE_COMPLETE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        IP.__name__,
        schema_constants.INSTANCES,
        self.ip._id,
        schema_constants.ATTRIBUTES,
        ip_fields.VALUE,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

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

    paths = extract_schema_paths(get_response.render(), null=False)

    expected_paths = [
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
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Payment.__name__,
        schema_constants.INSTANCES,
        payment._id,
        schema_constants.RELATIONSHIPS,
        payment_fields.ADDRESS,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_subscription_create(self):
    self.account.challenges.create(
      origin=subscription_create_constants.ORIGIN,
      is_open=False,
      has_been_used=False,
    )

    duration_in_days = 1
    activation_date = '1990-1-1 00:00:00UTC'

    create_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Subscription.__name__: {
            schema_constants.METHODS: {
              method_constants.CREATE: {
                subscription_fields.DURATION_IN_DAYS: duration_in_days,
                subscription_fields.ACTIVATION_DATE: activation_date,
              },
            },
          },
        },
      },
    }

    create_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=create_payload,
    )

    subscription = self.account.subscriptions.get(
      duration_in_days=duration_in_days,
      activation_date=parse_datetime(activation_date),
    )

    self.assertTrue(subscription is not None)

  def test_subscription_activate(self):
    subscription = self.account.subscriptions.create(
      duration_in_days=1,
      activation_date=parse_datetime('1990-1-1 00:00:00UTC'),
    )
    address = Address.objects.create(value='address_value', is_active=True)
    self.account.payments.create(
      address=address,
      origin=subscription.origin,
      is_open=False,
      has_been_used=False,
    )

    activate_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Subscription.__name__: {
            schema_constants.METHODS: {
              subscription_method_constants.ACTIVATE: {
                subscription_activate_constants.SUBSCRIPTION_ID: subscription._id,
              },
            },
          },
        },
      },
    }

    activate_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=activate_payload,
    )

    subscription.refresh_from_db()

    self.assertFalse(subscription.is_active)
    self.assertTrue(subscription.has_been_activated)

  def test_subscription_get(self):
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

    expected_paths = [
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
        self.subscription._id,
        schema_constants.ATTRIBUTES,
        subscription_fields.ORIGIN,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Subscription.__name__,
        schema_constants.INSTANCES,
        self.subscription._id,
        schema_constants.ATTRIBUTES,
        subscription_fields.DURATION_IN_DAYS,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Subscription.__name__,
        schema_constants.INSTANCES,
        self.subscription._id,
        schema_constants.ATTRIBUTES,
        subscription_fields.ACTIVATION_DATE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Subscription.__name__,
        schema_constants.INSTANCES,
        self.subscription._id,
        schema_constants.ATTRIBUTES,
        subscription_fields.IS_VALID_UNTIL,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Subscription.__name__,
        schema_constants.INSTANCES,
        self.subscription._id,
        schema_constants.ATTRIBUTES,
        subscription_fields.HAS_BEEN_ACTIVATED,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        Subscription.__name__,
        schema_constants.INSTANCES,
        self.subscription._id,
        schema_constants.ATTRIBUTES,
        subscription_fields.IS_ACTIVE,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_fee_report_create(self):
    self.account.challenges.create(
      origin=fee_report_create_constants.ORIGIN,
      is_open=False,
      has_been_used=False,
    )

    blocks_to_include = 1
    is_active = True

    create_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          FeeReport.__name__: {
            schema_constants.METHODS: {
              method_constants.CREATE: {
                fee_report_fields.BLOCKS_TO_INCLUDE: blocks_to_include,
                fee_report_fields.IS_ACTIVE: is_active,
              },
            },
          },
        },
      },
    }

    create_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=create_payload,
    )

    fee_report = self.account.fee_reports.get(
      blocks_to_include=blocks_to_include,
      is_active=is_active,
    )

    self.assertTrue(fee_report is not None)

  def test_fee_report_delete(self):
    self.account.challenges.create(
      origin=fee_report_delete_constants.ORIGIN,
      is_open=False,
      has_been_used=False,
    )
    fee_report = self.account.fee_reports.create(
      blocks_to_include=1,
      is_active=True,
    )

    delete_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          FeeReport.__name__: {
            schema_constants.METHODS: {
              method_constants.DELETE: {
                fee_report_delete_constants.FEE_REPORT_ID: fee_report._id,
              },
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

    self.assertFalse(self.account.fee_reports.filter(id=fee_report._id).exists())

  def test_fee_report_get(self):
    fee_report = self.account.fee_reports.create(
      blocks_to_include=1,
      is_active=True,
    )

    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          FeeReport.__name__: {
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

    expected_paths = [
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        fee_report_get_constants.FEE_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        fee_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.INSTANCES,
        fee_report._id,
        schema_constants.ATTRIBUTES,
        fee_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.INSTANCES,
        fee_report._id,
        schema_constants.ATTRIBUTES,
        fee_report_fields.IS_PROCESSING,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.INSTANCES,
        fee_report._id,
        schema_constants.ATTRIBUTES,
        fee_report_fields.BLOCKS_TO_INCLUDE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.INSTANCES,
        fee_report._id,
        schema_constants.ATTRIBUTES,
        fee_report_fields.AVERAGE_TX_FEE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.INSTANCES,
        fee_report._id,
        schema_constants.ATTRIBUTES,
        fee_report_fields.AVERAGE_TX_FEE_DENSITY,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.INSTANCES,
        fee_report._id,
        schema_constants.ATTRIBUTES,
        fee_report_fields.LAST_UPDATE_END_TIME,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        FeeReport.__name__,
        schema_constants.INSTANCES,
        fee_report._id,
        schema_constants.ATTRIBUTES,
        fee_report_fields.LATEST_BLOCK_HASH,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_transaction_report_create(self):
    self.account.challenges.create(
      origin=transaction_report_create_constants.ORIGIN,
      is_open=False,
      has_been_used=False,
    )

    is_active = True
    target_address = 'target_address'
    value_equal_to = 1

    create_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          TransactionReport.__name__: {
            schema_constants.METHODS: {
              method_constants.CREATE: {
                transaction_report_fields.IS_ACTIVE: is_active,
                transaction_report_fields.TARGET_ADDRESS: target_address,
                transaction_report_fields.VALUE_EQUAL_TO: value_equal_to,
              },
            },
          },
        },
      },
    }

    create_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=create_payload,
    )

    transaction_report = self.account.transaction_reports.get(
      is_active=is_active,
      target_address=target_address,
      value_equal_to=value_equal_to,
    )

    self.assertTrue(transaction_report is not None)

  def test_transaction_report_delete(self):
    self.account.challenges.create(
      origin=transaction_report_delete_constants.ORIGIN,
      is_open=False,
      has_been_used=False,
    )
    transaction_report = self.account.transaction_reports.create(
      is_active=True,
      target_address='target_address',
      value_equal_to=1,
    )

    delete_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          TransactionReport.__name__: {
            schema_constants.METHODS: {
              method_constants.DELETE: {
                transaction_report_delete_constants.TRANSACTION_REPORT_ID: transaction_report._id,
              },
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

    self.assertFalse(self.account.transaction_reports.filter(id=transaction_report._id).exists())

  def test_transaction_report_get(self):
    transaction_report = self.account.transaction_reports.create(
      is_active=True,
      target_address='target_address',
      value_equal_to=1,
    )

    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          TransactionReport.__name__: {
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

    expected_paths = [
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_report_get_constants.TRANSACTION_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.INSTANCES,
        transaction_report._id,
        schema_constants.ATTRIBUTES,
        transaction_report_fields.IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.INSTANCES,
        transaction_report._id,
        schema_constants.ATTRIBUTES,
        transaction_report_fields.TARGET_ADDRESS,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.INSTANCES,
        transaction_report._id,
        schema_constants.ATTRIBUTES,
        transaction_report_fields.VALUE_EQUAL_TO,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.INSTANCES,
        transaction_report._id,
        schema_constants.ATTRIBUTES,
        transaction_report_fields.VALUE_LESS_THAN,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.INSTANCES,
        transaction_report._id,
        schema_constants.ATTRIBUTES,
        transaction_report_fields.VALUE_GREATER_THAN,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionReport.__name__,
        schema_constants.INSTANCES,
        transaction_report._id,
        schema_constants.ATTRIBUTES,
        transaction_report_fields.LATEST_BLOCK_HASH,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_transaction_report_activate(self):
    self.account.challenges.create(
      origin=transaction_report_activate_constants.ORIGIN,
      is_open=False,
      has_been_used=False,
    )
    transaction_report = self.account.transaction_reports.create(
      is_active=True,
      target_address='target_address',
      value_equal_to=1,
    )

    activate_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          TransactionReport.__name__: {
            schema_constants.METHODS: {
              transaction_report_subscribed_method_constants.ACTIVATE: {
                transaction_report_activate_constants.TRANSACTION_REPORT_ID: transaction_report._id,
                transaction_report_fields.IS_ACTIVE: False,
              },
            },
          },
        },
      },
    }

    activate_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=activate_payload,
    )

    transaction_report.refresh_from_db()

    self.assertFalse(transaction_report.is_active)

  def test_transaction_match_get(self):
    transaction_report = self.account.transaction_reports.create(
      is_active=True,
      target_address='target_address',
      value_equal_to=1,
    )
    transaction_match = transaction_report.matches.create(
      is_new=True,
      block_hash='block_hash',
    )

    get_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          TransactionMatch.__name__: {
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

    expected_paths = [
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_get_constants.TRANSACTION_REPORT_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_get_constants.TRANSACTION_REPORT_TARGET_ADDRESS,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_get_constants.TRANSACTION_REPORT_IS_ACTIVE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_get_constants.TRANSACTION_MATCH_ID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_fields.IS_NEW,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.METHODS,
        method_constants.GET,
        transaction_match_fields.BLOCK_HASH,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.INSTANCES,
        transaction_match._id,
        schema_constants.ATTRIBUTES,
        transaction_match_fields.BLOCK_HASH,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.INSTANCES,
        transaction_match._id,
        schema_constants.ATTRIBUTES,
        transaction_match_fields.TXID,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.INSTANCES,
        transaction_match._id,
        schema_constants.ATTRIBUTES,
        transaction_match_fields.INDEX,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.INSTANCES,
        transaction_match._id,
        schema_constants.ATTRIBUTES,
        transaction_match_fields.VALUE,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.INSTANCES,
        transaction_match._id,
        schema_constants.ATTRIBUTES,
        transaction_match_fields.IS_NEW,
      ],
      [
        api_constants.SCHEMA,
        api_constants.MODELS,
        TransactionMatch.__name__,
        schema_constants.INSTANCES,
        transaction_match._id,
        schema_constants.RELATIONSHIPS,
        transaction_match_fields.TRANSACTION_REPORT,
      ],
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_transaction_match_dismiss(self):
    transaction_report = self.account.transaction_reports.create(
      is_active=True,
      target_address='target_address',
      value_equal_to=1,
    )
    transaction_match = transaction_report.matches.create(
      is_new=True,
      block_hash='block_hash',
    )

    dismiss_payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          TransactionMatch.__name__: {
            schema_constants.METHODS: {
              transaction_match_subscribed_method_constants.DISMISS: {},
            },
          },
        },
      },
    }

    dismiss_response = self.schema.respond(
      system=self.system,
      connection=self.connection,
      payload=dismiss_payload,
    )

    transaction_match.refresh_from_db()

    self.assertFalse(transaction_match.is_new)
