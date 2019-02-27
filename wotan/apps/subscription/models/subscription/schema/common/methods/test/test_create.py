
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants, with_challenge_errors
from ...... import Account, Challenge
from .....constants import subscription_fields
from ..constants import create_constants
from ..errors import create_errors
from ..create import SubscriptionCreateSchema

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class SubscriptionCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = SubscriptionCreateSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_create_no_arguments(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)
    challenge = Challenge.objects.get(origin=self.schema.origin)

    self.assertEqual(Challenge.objects.filter(origin=self.schema.origin, is_open=True).count(), 1)
    self.assertEqual(response.render(), {
      create_constants.CREATE_COMPLETE: False,
      with_challenge_constants.OPEN_CHALLENGE_ID: challenge._id,
    })

  def test_create(self):
    payload = {
      subscription_fields.DURATION_IN_DAYS: 31536000,
      subscription_fields.ACTIVATION_DATE: str(timezone.now()),
    }

    response = self.schema.respond(payload=payload, context=self.context)

    challenge = Challenge.objects.get(origin=self.schema.origin)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(Challenge.objects.filter(origin=self.schema.origin, is_open=False, has_been_used=True).count(), 1)
    self.assertEqual(second_response.render(), {
      create_constants.CREATE_COMPLETE: True,
    })

  def test_duration_not_included(self):
    first_response = self.schema.respond(payload={}, context=self.context)

    challenge = Challenge.objects.get(origin=self.schema.origin)

    challenge.is_open = False
    challenge.save()

    payload = {
      subscription_fields.ACTIVATION_DATE: str(timezone.now()),
    }

    response = self.schema.respond(payload=payload, context=self.context)

    duration_not_included = create_errors.DURATION_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        duration_not_included.code: duration_not_included.render(),
      },
    })
