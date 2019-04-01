
import uuid
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from .....constants import subscription_fields
from ..constants import get_constants
from ..errors import get_errors
from ..get import SubscriptionGetSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

  def get_account(self):
    return self.account

class SubscriptionGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = SubscriptionGetSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(account=self.account)
    self.active_subscription = self.account.subscriptions.create(is_active=True)
    self.inactive_subscription = self.account.subscriptions.create(is_active=False)

  def test_get_does_not_exist(self):
    subscription_id = uuid.uuid4().hex

    payload = {
      get_constants.SUBSCRIPTION_ID: subscription_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    subscription_does_not_exist = get_errors.SUBSCRIPTION_DOES_NOT_EXIST(id=subscription_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          subscription_does_not_exist.code: subscription_does_not_exist.render(),
        },
      },
    )

  def test_get(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.active_subscription,
        self.inactive_subscription,
      ]),
    )

  def test_get_id(self):
    payload = {
      get_constants.SUBSCRIPTION_ID: self.active_subscription._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_subscription],
    )

  def test_get_id_and_active(self):
    payload = {
      get_constants.SUBSCRIPTION_ID: self.active_subscription._id,
      subscription_fields.IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_subscription],
    )

  def test_get_active(self):
    payload = {
      subscription_fields.IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.active_subscription],
    )

  def test_get_inactive(self):
    payload = {
      subscription_fields.IS_ACTIVE: False,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [self.inactive_subscription],
    )
