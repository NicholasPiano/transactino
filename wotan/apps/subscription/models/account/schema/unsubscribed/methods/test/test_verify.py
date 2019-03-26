
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants
from ......challenge import Challenge
from ..... import Account
from ..verify import AccountVerifySchema
from ..constants import verify_constants
from ..errors import verify_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class AccountVerifySchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AccountVerifySchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.account.challenges.create(origin=verify_constants.ORIGIN, is_open=False, has_been_used=False)

  def test_verify_with_arguments(self):
    payload = {
      'key': 'value',
    }

    response = self.schema.respond(payload=payload, context=self.context)

    account_verify_takes_no_arguments = verify_errors.ACCOUNT_VERIFY_TAKES_NO_ARGUMENTS()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        account_verify_takes_no_arguments.code: account_verify_takes_no_arguments.render(),
      },
    })

  def test_verify_already_verified(self):
    self.account.is_verified = True
    self.account.save()
    response = self.schema.respond(payload={}, context=self.context)

    account_already_verified = verify_errors.ACCOUNT_ALREADY_VERIFIED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        account_already_verified.code: account_already_verified.render(),
      },
    })

  def test_verify(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.account.refresh_from_db()

    self.assertTrue(self.account.is_verified)
