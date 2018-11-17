
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.subscription.schema.with_challenge import with_challenge_constants, with_challenge_errors
from apps.subscription.models import Account, Challenge

from ..... import FeeReport
from .....constants import fee_report_fields
from ..activate import FeeReportActivateSchema
from ..constants import activate_constants
from ..errors import activate_errors

class TestContext():
  def __init__(self, account):
    self.account = account

class FeeReportActivateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = FeeReportActivateSchema(FeeReport)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_activate(self):
    fee_report = self.account.fee_reports.create()

    payload = {
      activate_constants.FEE_REPORT_ID: fee_report._id,
      fee_report_fields.IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(FeeReport.objects.filter(id=fee_report._id, is_active=False))

    challenge = Challenge.objects.get(origin=activate_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(FeeReport.objects.filter(id=fee_report._id, is_active=True))

  def test_activate_does_not_exist(self):
    test_id = uuid.uuid4().hex

    payload = {
      activate_constants.FEE_REPORT_ID: test_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    fee_report_does_not_exist = activate_errors.FEE_REPORT_DOES_NOT_EXIST(id=test_id)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        fee_report_does_not_exist.code: fee_report_does_not_exist.render(),
      },
    })

  def test_activate_id_not_included(self):
    payload = {
      fee_report_fields.IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    fee_report_id_not_included = activate_errors.FEE_REPORT_ID_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        fee_report_id_not_included.code: fee_report_id_not_included.render(),
      },
    })
