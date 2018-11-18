
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants, with_challenge_errors
from ......account import Account
from ......challenge import Challenge
from ..... import IP
from ..delete import IPDeleteSchema
from ..constants import delete_constants
from ..errors import delete_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class IPDeleteSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = IPDeleteSchema(IP)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_delete(self):
    payload = 'ip-value'

    ip = self.account.ips.create(value=payload)

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(IP.objects.filter(value=payload))

    challenge = Challenge.objects.get(origin=delete_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(IP.objects.filter(value=payload))

  def test_delete_does_not_exist(self):
    payload = 'ip-value'

    response = self.schema.respond(payload=payload, context=self.context)

    ip_does_not_exist = delete_errors.IP_DOES_NOT_EXIST(value=payload)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        ip_does_not_exist.code: ip_does_not_exist.render(),
      },
    })
