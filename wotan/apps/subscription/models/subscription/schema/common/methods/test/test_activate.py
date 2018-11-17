
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from util.api.constants import constants

from ...... import Account, Payment
from ..... import Subscription
from ..constants import activate_constants
from ..errors import activate_errors
from ..activate import SubscriptionActivateSchema

class TestContext():
  def __init__(self, account):
    self.account = account

class SubscriptionActivateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = SubscriptionActivateSchema()
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.activation_date = timezone.now()
    self.duration_in_days = 1
    self.subscription = self.account.subscriptions.create(
      activation_date=self.activation_date,
      duration_in_days=self.duration_in_days,
    )
    self.context = TestContext(self.account)

  def test_activate(self):
    payload = {
      activate_constants.SUBSCRIPTION_ID: self.subscription._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    payment = Payment.objects.get(origin=self.subscription.origin)

    payment.is_open = False
    payment.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      Payment.objects.filter(origin=self.subscription.origin, is_open=False, has_been_used=True).count(),
      1,
    )
    self.assertEqual(second_response.render(), {
      activate_constants.ACTIVATION_COMPLETE: True,
    })

  def test_subscription_without_subscription_id(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    subscription_id_not_included = activate_errors.SUBSCRIPTION_ID_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        subscription_id_not_included.code: subscription_id_not_included.render(),
      },
    })

  def test_subscription_does_not_exist(self):
    subscription_id = uuid.uuid4().hex
    payload = {
      activate_constants.SUBSCRIPTION_ID: subscription_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    subscription_does_not_exist = activate_errors.SUBSCRIPTION_DOES_NOT_EXIST(id=subscription_id)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        subscription_does_not_exist.code: subscription_does_not_exist.render(),
      },
    })
