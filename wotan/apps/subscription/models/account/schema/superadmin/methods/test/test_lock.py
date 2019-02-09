
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants, with_challenge_errors
from ......challenge import Challenge
from ..... import Account
from ..lock import AccountSuperadminLockSchema
from ..constants import lock_constants
from ..errors import account_superadmin_method_errors

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

  def test_lock(self):
    payload = {
      lock_constants.LOCK: True,
      lock_constants.ACCOUNT: self.account._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(Challenge.objects.filter(origin=lock_constants.ORIGIN, is_open=True).count(), 1)
    self.assertEqual(response.render(), {
      with_challenge_constants.OPEN_CHALLENGE_ID: Challenge.objects.get(origin=lock_constants.ORIGIN, is_open=True)._id,
      lock_constants.LOCKING_COMPLETE: False,
    })

  def test_lock_without_account(self):
    payload = {
      lock_constants.LOCK: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    account_not_included = account_superadmin_method_errors.ACCOUNT_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        account_not_included.code: account_not_included.render(),
      },
    })
    self.assertFalse(Challenge.objects.filter(origin=lock_constants.ORIGIN, is_open=True))

  def test_lock_open_challenge_exists(self):
    payload = {
      lock_constants.LOCK: True,
      lock_constants.ACCOUNT: self.account._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)
    second_response = self.schema.respond(payload=payload, context=self.context)

    challenge = Challenge.objects.get(origin=lock_constants.ORIGIN)

    open_challenge_exists_with_origin = with_challenge_errors.OPEN_CHALLENGE_EXISTS_WITH_ORIGIN(
      id=challenge._id,
      origin=lock_constants.ORIGIN,
    )
    self.assertEqual(second_response.render(), {
      constants.ERRORS: {
        open_challenge_exists_with_origin.code: open_challenge_exists_with_origin.render(),
      },
    })
    self.assertEqual(Challenge.objects.filter(origin=lock_constants.ORIGIN, is_open=True).count(), 1)
    self.assertFalse(self.account.is_superadmin_locked)

  def test_lock_with_solved_challenge(self):
    payload = {
      lock_constants.LOCK: True,
      lock_constants.ACCOUNT: self.account._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    challenge = Challenge.objects.get(origin=lock_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(Challenge.objects.filter(origin=lock_constants.ORIGIN, is_open=False, has_been_used=True).count(), 1)
    self.assertEqual(second_response.render(), {
      lock_constants.LOCKING_COMPLETE: True,
    })
    self.assertTrue(Account.objects.get().is_superadmin_locked)
