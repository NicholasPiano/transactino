
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants
from .......schema.with_payment import with_payment_constants
from ......address import Address
from ......account import Account
from ......challenge import Challenge
from ......payment import Payment
from ..... import IP
from .....constants import ip_fields
from ..create import IPCreateSchema
from ..constants import create_constants
from ..errors import create_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class IPCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.address = Address.objects.create(value='address_value', is_active=True)
    self.schema = IPCreateSchema(IP)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.ip_value = '123.123.123.123'

  def test_create_no_arguments(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=create_constants.ORIGIN).exists())

  def test_without_value(self):
    self.account.challenges.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)

    response = self.schema.respond(payload={}, context=self.context)

    value_not_included = create_errors.VALUE_NOT_INCLUDED()
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          value_not_included.code: value_not_included.render(),
        },
      },
    )

  def test_already_bound(self):
    self.account.challenges.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)

    self.account.ips.create(value=self.ip_value)
    payload = {
      ip_fields.VALUE: self.ip_value,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    ip_already_bound = create_errors.IP_ALREADY_BOUND(value=self.ip_value)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          ip_already_bound.code: ip_already_bound.render(),
        },
      },
    )

  def test_create_past_maximum(self):
    self.account.challenges.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)
    self.account.payments.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)

    for index in range(create_constants.MAX_IPS):
      self.account.ips.create(value='below-max-{}'.format(index))

    payload = {
      ip_fields.VALUE: self.ip_value,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(self.account.ips.count(), create_constants.MAX_IPS + 1)

  def test_create(self):
    self.account.challenges.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)

    payload = {
      ip_fields.VALUE: self.ip_value,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(self.account.ips.filter(value=self.ip_value))
