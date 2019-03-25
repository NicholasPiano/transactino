
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

  def test_without_report_id(self):
    challenge = self.account.challenges.create(origin=delete_constants.ORIGIN, is_open=False, has_been_used=False)
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    fee_report_id_not_included = delete_errors.FEE_REPORT_ID_NOT_INCLUDED()
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          fee_report_id_not_included.code: fee_report_id_not_included.render(),
        },
      },
    )

  def test_report_does_not_exist(self):
    challenge = self.account.challenges.create(origin=delete_constants.ORIGIN, is_open=False, has_been_used=False)
    fee_report_id = uuid.uuid4().hex
    payload = {
      delete_constants.FEE_REPORT_ID: fee_report_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    fee_report_does_not_exist = delete_errors.FEE_REPORT_DOES_NOT_EXIST(id=fee_report_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          fee_report_does_not_exist.code: fee_report_does_not_exist.render(),
        },
      },
    )

  def test_no_arguments(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=delete_constants.ORIGIN).exists())

  def test_delete(self):
    fee_report = self.account.fee_reports.create()

    payload = {
      delete_constants.FEE_REPORT_ID: fee_report._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(FeeReport.objects.get(id=fee_report._id))

    challenge = Challenge.objects.get(origin=delete_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(FeeReport.objects.get(id=fee_report._id))
