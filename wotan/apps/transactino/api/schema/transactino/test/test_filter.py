
import json

from django.conf import settings
from django.db import models
from django.test import TestCase
from django.utils import timezone

from util.gpg import GPG

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import filter_constants, method_constants
from apps.subscription.models import Account, IP, Connection
from apps.subscription.models.account.constants import account_fields

from ..constants import transactino_constants
from .. import TransactinoSchema

class FilterTestCase(TestCase):
  def setUp(self):
    self.schema = TransactinoSchema()
    self.account = Account.objects.create(
      is_superadmin=True,
      is_verified=True,
    )
    self.ip_value = 'ip_value'
    self.channel_name = 'channel_name'
    self.ip = self.account.ips.create(value=self.ip_value)
    self.connection, connection_created = Connection.objects.bring_online(
      name=self.channel_name,
      ip_value=self.ip_value,
    )

    Account.objects.create(public_key='something else')
    Account.objects.create(public_key='something more')
    Account.objects.create(public_key='something blue')
    Account.objects.create(public_key='green')
    Account.objects.create(public_key='something green')
    Account.objects.create(public_key='hello there')
    Account.objects.create(public_key='general kenobi')
    Account.objects.create(public_key='general kenobi green')
    Account.objects.create(public_key='general kenobi blue')

  def test_filter(self):
    payload = {
      transactino_constants.SCHEMA: {
        transactino_constants.MODELS: {
          Account.__name__: {
            schema_constants.METHODS: {
              method_constants.FILTER: {
                filter_constants.COMPOSITE: [
                  {
                    filter_constants.KEY: 'public_key__contains',
                    filter_constants.VALUE: 'green',
                  },
                  {
                    filter_constants.AND: [
                      {
                        filter_constants.KEY: 'public_key__contains',
                        filter_constants.VALUE: 'general',
                      },
                      {
                        filter_constants.AND: [],
                        filter_constants.KEY: 'public_key__contains',
                        filter_constants.VALUE + 'error': 'kenobi',
                      },
                    ],
                  },
                ],
              },
            },
          },
        },
      },
    }

    response = self.schema.respond(connection=self.connection, payload=payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(False)
