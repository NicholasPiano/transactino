
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
from ..create import TransactionReportCreateSchema
from ..constants import create_constants
from ..errors import create_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class TransactionReportCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = TransactionReportCreateSchema(TransactionReport)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_no_arguments(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=create_constants.ORIGIN).exists())
    self.assertFalse(TransactionReport.objects.exists())

  def test_without_target_address(self):
    challenge = self.account.challenges.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    target_address_not_included = create_errors.TARGET_ADDRESS_NOT_INCLUDED()
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          target_address_not_included.code: target_address_not_included.render(),
        },
      },
    )

  def test_with_equal_and_range(self):
    challenge = self.account.challenges.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)
    payload = {
      transaction_report_fields.TARGET_ADDRESS: 'target_address',
      transaction_report_fields.VALUE_EQUAL_TO: 'equal',
      transaction_report_fields.VALUE_LESS_THAN: 'less',
      transaction_report_fields.VALUE_GREATER_THAN: 'greater',
    }

    response = self.schema.respond(payload=payload, context=self.context)

    equal_used_with_range = create_errors.EQUAL_USED_WITH_RANGE()
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          equal_used_with_range.code: equal_used_with_range.render(),
        },
      },
    )

  def test_with_invalid_range(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertFalse(TransactionReport.objects.exists())

    challenge = Challenge.objects.get(origin=create_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    target_address = 'target_address'
    value_less_than = 1
    value_greater_than = 2
    is_active = True

    payload = {
      transaction_report_fields.TARGET_ADDRESS: target_address,
      transaction_report_fields.VALUE_LESS_THAN: value_less_than,
      transaction_report_fields.VALUE_GREATER_THAN: value_greater_than,
      transaction_report_fields.IS_ACTIVE: is_active,
    }

    second_response = self.schema.respond(payload=payload, context=self.context)

    invalid_value_range = create_errors.INVALID_VALUE_RANGE(
      lower_bound=value_greater_than,
      upper_bound=value_less_than,
    )
    self.assertEqual(
      second_response.render(),
      {
        constants.ERRORS: {
          invalid_value_range.code: invalid_value_range.render(),
        },
      },
    )

  def test_create(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertFalse(TransactionReport.objects.exists())

    challenge = Challenge.objects.get(origin=create_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    target_address = 'target_address'
    value_equal_to = 1
    is_active = True

    payload = {
      transaction_report_fields.TARGET_ADDRESS: target_address,
      transaction_report_fields.VALUE_EQUAL_TO: value_equal_to,
      transaction_report_fields.IS_ACTIVE: is_active,
    }

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(
      TransactionReport.objects.filter(
        target_address=target_address,
        value_equal_to=value_equal_to,
        is_active=is_active,
      ).exists(),
    )
