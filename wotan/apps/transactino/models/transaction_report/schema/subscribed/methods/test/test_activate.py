
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.subscription.schema.with_challenge import with_challenge_constants, with_challenge_errors
from apps.subscription.models import Account, Challenge

from ..... import TransactionReport
from .....constants import transaction_report_fields
from ..activate import TransactionReportActivateSchema
from ..constants import activate_constants
from ..errors import activate_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class TransactionReportActivateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = TransactionReportActivateSchema(TransactionReport)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_without_report_id(self):
    challenge = self.account.challenges.create(origin=activate_constants.ORIGIN, is_open=False, has_been_used=False)
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    transaction_report_id_not_included = activate_errors.TRANSACTION_REPORT_ID_NOT_INCLUDED()
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          transaction_report_id_not_included.code: transaction_report_id_not_included.render(),
        },
      },
    )

  def test_report_does_not_exist(self):
    challenge = self.account.challenges.create(origin=activate_constants.ORIGIN, is_open=False, has_been_used=False)
    transaction_report_id = uuid.uuid4().hex
    payload = {
      activate_constants.TRANSACTION_REPORT_ID: transaction_report_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    transaction_report_does_not_exist = activate_errors.TRANSACTION_REPORT_DOES_NOT_EXIST(id=transaction_report_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          transaction_report_does_not_exist.code: transaction_report_does_not_exist.render(),
        },
      },
    )

  def test_no_arguments(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=activate_constants.ORIGIN).exists())

  def test_activate(self):
    is_active = True
    transaction_report = self.account.transaction_reports.create(is_active=not is_active)

    payload = {
      activate_constants.TRANSACTION_REPORT_ID: transaction_report._id,
      transaction_report_fields.IS_ACTIVE: is_active,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(TransactionReport.objects.get(id=transaction_report._id).is_active, not is_active)

    challenge = Challenge.objects.get(origin=activate_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(TransactionReport.objects.get(id=transaction_report._id).is_active, is_active)

  def test_activate_without_active(self):
    transaction_report = self.account.transaction_reports.create(is_active=False)

    payload = {
      activate_constants.TRANSACTION_REPORT_ID: transaction_report._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(TransactionReport.objects.get(id=transaction_report._id).is_active, False)

    challenge = Challenge.objects.get(origin=activate_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(TransactionReport.objects.get(id=transaction_report._id).is_active, True)
