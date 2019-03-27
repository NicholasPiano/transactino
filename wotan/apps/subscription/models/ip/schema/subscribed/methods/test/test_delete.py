
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
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

  def test_no_arguments(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=delete_constants.ORIGIN).exists())

  def test_without_ip_id(self):
    challenge = self.account.challenges.create(origin=delete_constants.ORIGIN, is_open=False, has_been_used=False)
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    ip_id_not_included = delete_errors.IP_ID_NOT_INCLUDED()
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          ip_id_not_included.code: ip_id_not_included.render(),
        },
      },
    )

  def test_ip_does_not_exist(self):
    challenge = self.account.challenges.create(origin=delete_constants.ORIGIN, is_open=False, has_been_used=False)
    ip_id = uuid.uuid4().hex
    payload = {
      delete_constants.IP_ID: ip_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    ip_does_not_exist = delete_errors.IP_DOES_NOT_EXIST(id=ip_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          ip_does_not_exist.code: ip_does_not_exist.render(),
        },
      },
    )

  def test_delete(self):
    challenge = self.account.challenges.create(origin=delete_constants.ORIGIN, is_open=False, has_been_used=False)
    ip = self.account.ips.create()

    payload = {
      delete_constants.IP_ID: ip._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(self.account.ips.get(id=ip._id))
