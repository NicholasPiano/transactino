
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants, with_challenge_errors
from ......challenge import Challenge
from ..... import Account
from ..delete import AccountDeleteSchema
from ..constants import delete_constants
from ..errors import delete_errors

class TestContext():
  def __init__(self, account):
    self.account = account

class AccountDeleteSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AccountDeleteSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_delete(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    challenge = Challenge.objects.get(origin=delete_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(Challenge.objects.all())
    self.assertFalse(Account.objects.all())
    self.assertEqual(second_response.render(), {
      delete_constants.DELETION_COMPLETE: True,
    })

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
