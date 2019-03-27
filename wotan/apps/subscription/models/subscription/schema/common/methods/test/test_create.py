
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants, with_challenge_errors
from ...... import Account, Challenge
from .....constants import subscription_fields
from ..constants import create_constants
from ..errors import create_errors
from ..create import SubscriptionCreateSchema

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class SubscriptionCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = SubscriptionCreateSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_create_no_arguments(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=self.schema.origin).exists())

  def test_duration_not_included(self):
    self.account.challenges.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)

    payload = {
      subscription_fields.ACTIVATION_DATE: str(timezone.now()),
    }

    response = self.schema.respond(payload=payload, context=self.context)

    duration_not_included = create_errors.DURATION_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        duration_not_included.code: duration_not_included.render(),
      },
    })

  def test_create(self):
    self.account.challenges.create(origin=create_constants.ORIGIN, is_open=False, has_been_used=False)

    duration_in_days = 31536000

    payload = {
      subscription_fields.DURATION_IN_DAYS: duration_in_days,
      subscription_fields.ACTIVATION_DATE: str(timezone.now()),
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(self.account.subscriptions.filter(duration_in_days=duration_in_days).exists())
