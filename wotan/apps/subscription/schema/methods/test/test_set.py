
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

class AccountSuperadminSetSchemaTestCase(TestCase):
  def setUp(self):
    self.origin = uuid.uuid4().hex
    self.schema = SetSchemaWithChallenge(Account, origin=self.origin)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_set(self):
    self.assertFalse(self.account.is_verified)

    payload = {
      self.account._id: {
        schema_constants.ATTRIBUTES: {
          account_fields.IS_VERIFIED: True,
        },
      }
    }

    response = self.schema.respond(payload=payload, context=self.context)

    challenge = Challenge.objects.get(origin=self.origin)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.account.refresh_from_db()

    self.assertTrue(self.account.is_verified)
