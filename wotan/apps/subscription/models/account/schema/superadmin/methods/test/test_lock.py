
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants
from ......challenge import Challenge
from ..... import Account
from ..lock import AccountSuperadminLockSchema
from ..constants import lock_constants
from ..errors import lock_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class AccountSuperadminLockSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AccountSuperadminLockSchema(Account)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.account.challenges.create(origin=lock_constants.ORIGIN, is_open=False, has_been_used=False)

  def test_lock_without_account_id(self):
    payload = {
      lock_constants.LOCK: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    account_id_not_included = lock_errors.ACCOUNT_ID_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        account_id_not_included.code: account_id_not_included.render(),
      },
    })

  def test_lock(self):
    payload = {
      lock_constants.LOCK: True,
      lock_constants.ACCOUNT_ID: self.account._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.account.refresh_from_db()

    self.assertTrue(self.account.is_superadmin_locked)
