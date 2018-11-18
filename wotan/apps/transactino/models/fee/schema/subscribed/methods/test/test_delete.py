
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.subscription.schema.with_challenge import with_challenge_constants, with_challenge_errors
from apps.subscription.models import Account, Challenge

from ..... import FeeReport
from ..delete import FeeReportDeleteSchema
from ..constants import delete_constants
from ..errors import delete_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class FeeReportDeleteSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = FeeReportDeleteSchema(FeeReport)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_delete(self):
    fee_report = self.account.fee_reports.create()

    payload = fee_report._id

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(FeeReport.objects.filter(id=payload))

    challenge = Challenge.objects.get(origin=delete_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(FeeReport.objects.filter(id=payload))

  def test_delete_does_not_exist(self):
    payload = uuid.uuid4().hex

    response = self.schema.respond(payload=payload, context=self.context)

    fee_report_does_not_exist = delete_errors.FEE_REPORT_DOES_NOT_EXIST(id=payload)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        fee_report_does_not_exist.code: fee_report_does_not_exist.render(),
      },
    })
