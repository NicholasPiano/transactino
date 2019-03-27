
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from ......challenge import Challenge
from ..... import IP
from ..get import IPGetSchema
from ..constants import get_constants
from ..errors import get_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class IPGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = IPGetSchema(IP)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.account.challenges.create(origin=get_constants.ORIGIN, is_open=False, has_been_used=False)

  def test_get_with_arguments(self):
    payload = {
      'key': 'value',
    }

    response = self.schema.respond(payload=payload, context=self.context)

    ip_get_takes_no_arguments = get_errors.IP_GET_TAKES_NO_ARGUMENTS()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        ip_get_takes_no_arguments.code: ip_get_takes_no_arguments.render(),
      },
    })

  def test_get(self):
    ip = self.account.ips.create(value='ip-address')

    response = self.schema.respond(payload={}, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [ip],
    )
