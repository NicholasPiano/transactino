
import json

from django.conf import settings
from django.test import TestCase

from util.extract_schema_paths import extract_schema_paths

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants
from apps.subscription.models import Connection, Account
from apps.subscription.models.account.constants import account_fields

from ..constants import transactino_constants
from .. import TransactinoSchema

class AnonymousTestCase(TestCase):
  def setUp(self):
    self.schema = TransactinoSchema()
    self.public_key = settings.TEST_PUBLIC_KEY
    self.ip_value = 'ip_value'
    self.channel_name = 'channel_name'
    self.connection, connection_created = Connection.objects.bring_online(
      name=self.channel_name,
      ip_value=self.ip_value,
    )

  def test_schema_paths(self):
    null_payload = None

    response = self.schema.respond(payload=null_payload, connection=self.connection)
    rendered_response = response.render()
    paths = extract_schema_paths(rendered_response)

    self.assertEqual(
      paths,
      [
        [
          transactino_constants.SCHEMA,
          transactino_constants.MODELS,
          Account.__name__,
          schema_constants.METHODS,
          method_constants.CREATE,
          account_fields.PUBLIC_KEY,
        ],
      ],
    )

  def test_account_create(self):
    create_payload = {
      transactino_constants.SCHEMA: {
        transactino_constants.MODELS: {
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
