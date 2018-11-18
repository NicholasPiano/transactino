
import uuid
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from ..constants import respond_constants
from ..errors import respond_errors
from ..respond import ChallengeRespondSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

  def get_account(self):
    return self.account

class ChallengeRespondSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = ChallengeRespondSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.challenge = self.account.challenges.create()
    self.challenge.encrypt_content()
    self.context = TestContext(account=self.account)

  def test_respond(self):
    payload = {
      respond_constants.CHALLENGE_ID: self.challenge._id,
      respond_constants.PLAINTEXT: self.challenge.content,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(response.render(), {
      respond_constants.CHALLENGE_ID: self.challenge._id,
      respond_constants.IS_VERIFIED: True,
    })

  def test_id_not_included(self):
    payload = {
      respond_constants.PLAINTEXT: self.challenge.content,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    challenge_id_not_included = respond_errors.CHALLENGE_ID_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        challenge_id_not_included.code: challenge_id_not_included.render(),
      },
    })

  def test_challenge_does_not_exist(self):
    test_id = uuid.uuid4().hex
    payload = {
      respond_constants.CHALLENGE_ID: test_id,
      respond_constants.PLAINTEXT: self.challenge.content,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    challenge_does_not_exist = respond_errors.CHALLENGE_DOES_NOT_EXIST(id=test_id)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        challenge_does_not_exist.code: challenge_does_not_exist.render(),
      },
    })

  def test_challenge_has_been_used(self):
    self.challenge.has_been_used = True
    self.challenge.save()

    payload = {
      respond_constants.CHALLENGE_ID: self.challenge._id,
      respond_constants.PLAINTEXT: self.challenge.content,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    closed_challenge_has_been_used = respond_errors.CLOSED_CHALLENGE_HAS_BEEN_USED(id=self.challenge._id)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        closed_challenge_has_been_used.code: closed_challenge_has_been_used.render(),
      },
    })

  def test_armor_and_plaintext_included(self):
    payload = {
      respond_constants.CHALLENGE_ID: self.challenge._id,
      respond_constants.PLAINTEXT: self.challenge.content,
      respond_constants.ARMOR: 'armor',
    }

    response = self.schema.respond(payload=payload, context=self.context)

    armor_and_plaintext_included = respond_errors.ARMOR_AND_PLAINTEXT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        armor_and_plaintext_included.code: armor_and_plaintext_included.render(),
      },
    })

  def test_armor_or_plaintext_not_included(self):
    payload = {
      respond_constants.CHALLENGE_ID: self.challenge._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    armor_or_plaintext_not_included = respond_errors.ARMOR_OR_PLAINTEXT_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        armor_or_plaintext_not_included.code: armor_or_plaintext_not_included.render(),
      },
    })

  def test_content_mismatch(self):
    payload = {
      respond_constants.CHALLENGE_ID: self.challenge._id,
      respond_constants.PLAINTEXT: 'bad-content',
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(response.render(), {
      respond_constants.CHALLENGE_ID: self.challenge._id,
      respond_constants.IS_VERIFIED: False,
    })