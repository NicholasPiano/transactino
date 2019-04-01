
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
    self.first_ip = self.account.ips.create(value='first')
    self.second_ip = self.account.ips.create(value='second')

  def test_get_does_not_exist(self):
    ip_id = uuid.uuid4().hex
    payload = {
      get_constants.IP_ID: ip_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    ip_does_not_exist = get_errors.IP_DOES_NOT_EXIST(id=ip_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          ip_does_not_exist.code: ip_does_not_exist.render(),
        },
      },
    )

  def test_get_with_id(self):
    payload = {
      get_constants.IP_ID: self.first_ip._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(self.first_ip in response.internal_queryset)

  def test_get(self):
    response = self.schema.respond(payload={}, context=self.context)

    expected_queryset = [
      self.first_ip,
      self.second_ip,
    ]

    self.assertEqual(len(response.internal_queryset), len(expected_queryset))
    for result in response.internal_queryset:
      self.assertTrue(result in expected_queryset)
