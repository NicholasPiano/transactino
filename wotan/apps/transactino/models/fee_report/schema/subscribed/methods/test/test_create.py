
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

  def test_no_arguments(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=create_constants.ORIGIN).exists())
    self.assertFalse(FeeReport.objects.exists())

  def test_create(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertFalse(FeeReport.objects.exists())

    challenge = Challenge.objects.get(origin=create_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    payload = {}

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(FeeReport.objects.filter(blocks_to_include=1, is_active=True).exists())
