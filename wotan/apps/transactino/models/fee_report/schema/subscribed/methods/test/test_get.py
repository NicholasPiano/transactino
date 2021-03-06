
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.base.constants import model_fields
from apps.subscription.models import Account, Challenge

from ..... import FeeReport
from .....constants import fee_report_fields
from ..constants import get_constants
from ..errors import get_errors
from ..get import FeeReportGetSchema

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class FeeReportGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = FeeReportGetSchema(FeeReport)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.active_fee_report = self.account.fee_reports.create(is_active=True)
    self.inactive_fee_report = self.account.fee_reports.create(is_active=False)

  def test_get_does_not_exist(self):
    fee_report_id = uuid.uuid4().hex

    payload = {
      get_constants.FEE_REPORT_ID: fee_report_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    fee_report_does_not_exist = get_errors.FEE_REPORT_DOES_NOT_EXIST(id=fee_report_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          fee_report_does_not_exist.code: fee_report_does_not_exist.render(),
        },
      },
    )

  def test_get(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.inactive_fee_report,
        self.active_fee_report,
      ]),
    )

  def test_get_id(self):
    payload = {
      get_constants.FEE_REPORT_ID: self.active_fee_report._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_fee_report],
    )

  def test_get_id_and_active(self):
    payload = {
      get_constants.FEE_REPORT_ID: self.active_fee_report._id,
      fee_report_fields.IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_fee_report],
    )

  def test_get_active(self):
    payload = {
      fee_report_fields.IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_fee_report],
    )

  def test_get_inactive(self):
    payload = {
      fee_report_fields.IS_ACTIVE: False,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.inactive_fee_report],
    )
