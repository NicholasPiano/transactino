
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
from ..create import FeeReportCreateSchema
from ..constants import create_constants

FeeReport.process = lambda self: 'mock'
FeeReport.schedule_process = lambda self: 'mock'
FeeReport.unschedule = lambda self: 'mock'

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class FeeReportCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = FeeReportCreateSchema(FeeReport)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_create(self):
    blocks_to_include = 5
    is_active = True

    payload = {
      fee_report_fields.BLOCKS_TO_INCLUDE: blocks_to_include,
      fee_report_fields.IS_ACTIVE: is_active,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(FeeReport.objects.filter(
      blocks_to_include=blocks_to_include,
      is_active=is_active,
    ))

    challenge = Challenge.objects.get(origin=create_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(FeeReport.objects.filter(
      blocks_to_include=blocks_to_include,
      is_active=is_active,
    ))
