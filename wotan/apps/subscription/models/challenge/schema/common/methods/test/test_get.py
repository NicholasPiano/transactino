
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from .....constants import challenge_fields
from ..get import ChallengeGetSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

class ChallengeGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = ChallengeGetSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(account=self.account)
    self.open_challenge = self.account.challenges.create(is_open=True)
    self.closed_challenge = self.account.challenges.create(is_open=False)

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
