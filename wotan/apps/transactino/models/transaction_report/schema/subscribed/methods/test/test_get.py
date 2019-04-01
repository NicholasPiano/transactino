
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.base.constants import model_fields
from apps.subscription.models import Account, Challenge

from ..... import TransactionReport
from .....constants import transaction_report_fields
from ..constants import get_constants
from ..get import TransactionReportGetSchema

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class TransactionReportGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = TransactionReportGetSchema(TransactionReport)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.active_transaction_report = self.account.transaction_reports.create(is_active=True)
    self.inactive_transaction_report = self.account.transaction_reports.create(is_active=False)

  def test_get(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.inactive_transaction_report,
        self.active_transaction_report,
      ]),
    )

  def test_get_id(self):
    payload = {
      get_constants.TRANSACTION_REPORT_ID: self.active_transaction_report._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_transaction_report],
    )

  def test_get_id_and_active(self):
    payload = {
      get_constants.TRANSACTION_REPORT_ID: self.active_transaction_report._id,
      transaction_report_fields.IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_transaction_report],
    )

  def test_get_active(self):
    payload = {
      transaction_report_fields.IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_transaction_report],
    )

  def test_get_inactive(self):
    payload = {
      transaction_report_fields.IS_ACTIVE: False,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.inactive_transaction_report],
    )
