
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.base.schema.constants import schema_constants

from ....models.challenge import Challenge
from ....models.account import Account
from ....models.account.constants import account_fields
from ..set import SetSchemaWithChallenge
from ..constants import set_constants

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class SubscriptionSetTestCase(TestCase):
  def setUp(self):
    self.origin = uuid.uuid4().hex
    self.schema = SetSchemaWithChallenge(Account, origin=self.origin)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_without_arguments(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=self.origin).exists())

  def test_set(self):
    self.account.challenges.create(origin=self.origin, is_open=False, has_been_used=False)
    self.assertFalse(self.account.is_verified)

    payload = {
      self.account._id: {
        schema_constants.ATTRIBUTES: {
          account_fields.IS_VERIFIED: True,
        },
      }
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.account.refresh_from_db()

    self.assertTrue(self.account.is_verified)
