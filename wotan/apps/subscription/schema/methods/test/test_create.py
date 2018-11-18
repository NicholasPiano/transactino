
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
from ..create import CreateSchemaWithChallenge
from ..constants import create_constants

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class AccountSuperadminSetSchemaTestCase(TestCase):
  def setUp(self):
    self.origin = uuid.uuid4().hex
    self.schema = CreateSchemaWithChallenge(Address, origin=self.origin)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_set(self):
    self.assertFalse(Address.objects.get())

    temp_id = uuid.uuid4().hex
    payload = {
      temp_id: {
        schema_constants.ATTRIBUTES: {
          address_fields.VALUE: 'address-value',
        },
      }
    }

    response = self.schema.respond(payload=payload, context=self.context)

    challenge = Challenge.objects.get(origin=self.origin)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    address = Address.objects.get()
    self.assertTrue(address)
    self.assertEqual(second_response.render(), {
      create_constants.CREATE_COMPLETE: True,
      create_constants.CREATED: {
        temp_id: address._id,
      },
    })
