
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants
from ......challenge import Challenge
from ..... import Account
from ..lock import AccountSubscribedLockSchema
from ..constants import lock_constants

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class AccountSubscribedLockSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AccountSubscribedLockSchema(Account)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.account.challenges.create(origin=lock_constants.ORIGIN, is_open=False, has_been_used=False)

  def test_lock(self):
    payload = {
      lock_constants.LOCK: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertTrue(Account.objects.get().is_locked)
