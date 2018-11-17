
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants, with_challenge_errors
from .......schema.with_payment import with_payment_constants, with_payment_errors
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

class IPCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = IPCreateSchema(IP)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_create(self):
    ip_value = 'ip-value'

    payload = {
      ip_fields.VALUE: ip_value,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(IP.objects.filter(value=ip_value))

    challenge = Challenge.objects.get(origin=create_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(IP.objects.filter(value=ip_value))
    self.assertFalse(Payment.objects.filter(origin=create_constants.ORIGIN))

  def test_create_without_value(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    value_not_included = create_errors.VALUE_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        value_not_included.code: value_not_included.render(),
      },
    })

  def test_create_already_bound(self):
    second_account = Account.objects.create()
    bound_ip_value = 'bound_ip_value'
    bound_ip = second_account.ips.create(value=bound_ip_value)
    payload = {
      ip_fields.VALUE: bound_ip_value,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    ip_already_bound = create_errors.IP_ALREADY_BOUND(value=bound_ip_value)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        ip_already_bound.code: ip_already_bound.render(),
      },
    })

  def test_create_past_maximum(self):
    for index in range(create_constants.MAX_IPS):
      self.account.ips.create(value='below-max-{}'.format(index))

    ip_value = 'ip-value'

    payload = {
      ip_fields.VALUE: ip_value,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(IP.objects.filter(value=ip_value))

    challenge = Challenge.objects.get(origin=create_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(IP.objects.filter(value=ip_value))

    payment = Payment.objects.get(origin=create_constants.ORIGIN)

    payment.is_open = False
    payment.save()

    third_response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(IP.objects.filter(value=ip_value))
