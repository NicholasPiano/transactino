
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from .....constants import payment_fields
from ..constants import get_constants
from ..get import PaymentGetSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

  def get_account(self):
    return self.account

class PaymentGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = PaymentGetSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(account=self.account)
    self.open_payment = self.account.payments.create(is_open=True)
    self.closed_payment = self.account.payments.create(is_open=False)

  def test_get(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.open_payment,
        self.closed_payment,
      ]),
    )

  def test_get_id(self):
    payload = {
      get_constants.PAYMENT_ID: self.open_payment._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.open_payment],
    )

  def test_get_id_with_open(self):
    payload = {
      get_constants.PAYMENT_ID: self.open_payment._id,
      payment_fields.IS_OPEN: False,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.open_payment],
    )

  def test_get_open(self):
    payload = {
      payment_fields.IS_OPEN: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.open_payment],
    )

  def test_get_closed(self):
    payload = {
      payment_fields.IS_OPEN: False,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.closed_payment],
    )
