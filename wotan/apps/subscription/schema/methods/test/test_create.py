
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.base.schema.constants import schema_constants

from ....models.challenge import Challenge
from ....models.account import Account
from ....models.address import Address
from ....models.address.constants import address_fields
from ...with_challenge.constants import with_challenge_constants
from ..create import CreateSchemaWithChallenge
from ..constants import create_constants

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class SubscriptionCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.origin = uuid.uuid4().hex
    self.schema = CreateSchemaWithChallenge(Address, origin=self.origin)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_without_arguments(self):
    response = self.schema.respond(payload={}, context=self.context)

    self.assertTrue(self.account.challenges.filter(origin=self.origin).exists())

  def test_create(self):
    self.account.challenges.create(origin=self.origin, is_open=False, has_been_used=False)
    self.assertFalse(Address.objects.exists())

    temp_id = uuid.uuid4().hex
    payload = {
      temp_id: {
        schema_constants.ATTRIBUTES: {
          address_fields.VALUE: 'address-value',
        },
      }
    }

    response = self.schema.respond(payload=payload, context=self.context)

    address = Address.objects.get()
    self.assertTrue(address)
    self.assertEqual(response.render(), {
      create_constants.CREATED: {
        temp_id: address._id,
      },
    })
