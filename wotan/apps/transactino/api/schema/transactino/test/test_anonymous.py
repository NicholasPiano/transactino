
import json

from django.conf import settings
from django.test import TestCase

from util.extract_schema_paths import extract_schema_paths

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants
from apps.subscription.models import Connection, Account, System
from apps.subscription.models.account.constants import account_fields
from apps.subscription.models.system.constants import system_fields

from ....constants import api_constants
from ..constants import transactino_constants
from .. import TransactinoSchema

class AnonymousTestCase(TestCase):
  def setUp(self):
    self.schema = TransactinoSchema()
    self.system = System.objects.create_and_import(
      public_key=settings.TEST_SYSTEM_PUBLIC_KEY,
      private_key=settings.TEST_SYSTEM_PRIVATE_KEY,
    )
    self.public_key = settings.TEST_PUBLIC_KEY
    self.ip_value = 'ip_value'
    self.channel_name = 'channel_name'
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
        api_constants.MODELS,
        Account.__name__,
        schema_constants.METHODS,
        method_constants.CREATE,
        account_fields.PUBLIC_KEY,
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
    ]

    self.assertEqual(len(paths), len(expected_paths))
    for path in paths:
      print('PATH... ', path)
      self.assertTrue(path in expected_paths)

  def test_account_create(self):
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
      system=self.system,
      connection=self.connection,
      payload=create_payload,
    )

    self.assertTrue(Account.objects.filter(public_key=self.public_key))

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
