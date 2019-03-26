
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants
from ......challenge import Challenge
from ..... import Account
from ..delete import AccountDeleteSchema
from ..constants import delete_constants
from ..errors import delete_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class AccountDeleteSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AccountDeleteSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.account.challenges.create(origin=delete_constants.ORIGIN, is_open=False, has_been_used=False)

  def test_delete_with_arguments(self):
    payload = {
      'key': 'value',
    }

    response = self.schema.respond(payload=payload, context=self.context)

    account_delete_takes_no_arguments = delete_errors.ACCOUNT_DELETE_TAKES_NO_ARGUMENTS()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        account_delete_takes_no_arguments.code: account_delete_takes_no_arguments.render(),
      },
    })

  def test_delete(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertFalse(Account.objects.all())
    self.assertEqual(response.render(), {
      with_challenge_constants.CHALLENGE_COMPLETE: True,
    })
