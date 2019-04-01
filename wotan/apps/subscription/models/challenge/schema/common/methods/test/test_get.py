
import uuid
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from .....constants import challenge_fields
from ..constants import get_constants
from ..errors import get_errors
from ..get import ChallengeGetSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

  def get_account(self):
    return self.account

class ChallengeGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = ChallengeGetSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(account=self.account)
    self.open_challenge = self.account.challenges.create(is_open=True)
    self.closed_challenge = self.account.challenges.create(is_open=False)

  def test_get_does_not_exist(self):
    challenge_id = uuid.uuid4().hex

    payload = {
      get_constants.CHALLENGE_ID: challenge_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    challenge_does_not_exist = get_errors.CHALLENGE_DOES_NOT_EXIST(id=challenge_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          challenge_does_not_exist.code: challenge_does_not_exist.render(),
        },
      },
    )

  def test_get(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [
        self.open_challenge,
        self.closed_challenge,
      ],
    )

  def test_get_id(self):
    payload = {
      get_constants.CHALLENGE_ID: self.open_challenge._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.open_challenge],
    )

  def test_get_id_and_open(self):
    payload = {
      get_constants.CHALLENGE_ID: self.open_challenge._id,
      challenge_fields.IS_OPEN: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.open_challenge],
    )

  def test_get_open(self):
    payload = {
      challenge_fields.IS_OPEN: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.open_challenge],
    )

  def test_get_closed(self):
    payload = {
      challenge_fields.IS_OPEN: False,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.closed_challenge],
    )
