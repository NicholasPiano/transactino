
import uuid
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from .....constants import challenge_fields
from ..constants import delete_constants
from ..errors import delete_errors
from ..delete import ChallengeDeleteSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

  def get_account(self):
    return self.account

class ChallengeDeleteSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = ChallengeDeleteSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(account=self.account)
    self.challenge = self.account.challenges.create(is_open=True)

  def test_delete_id_not_included(self):
    response = self.schema.respond(payload={}, context=self.context)

    challenge_id_not_included = delete_errors.CHALLENGE_ID_NOT_INCLUDED()
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          challenge_id_not_included.code: challenge_id_not_included.render(),
        },
      },
    )

  def test_delete_does_not_exist(self):
    challenge_id = uuid.uuid4().hex

    payload = {
      delete_constants.CHALLENGE_ID: challenge_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    challenge_does_not_exist = delete_errors.CHALLENGE_DOES_NOT_EXIST(id=challenge_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          challenge_does_not_exist.code: challenge_does_not_exist.render(),
        },
      },
    )

  def test_delete(self):
    payload = {
      delete_constants.CHALLENGE_ID: self.challenge._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertFalse(self.account.challenges.filter(id=self.challenge._id).exists())
