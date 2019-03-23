
import uuid
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from .....constants import address_fields
from ..... import Address
from ..constants import get_constants
from ..errors import get_errors
from ..get import AddressGetSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

  def get_account(self):
    return self.account

class AddressGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AddressGetSchema(Address)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(account=self.account)

  def test_get_with_no_id(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    address_id_not_included = get_errors.ADDRESS_ID_NOT_INCLUDED()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        address_id_not_included.code: address_id_not_included.render(),
      },
    })

  def test_get_address_does_not_exist(self):
    address_id = uuid.uuid4()
    payload = {
      get_constants.ADDRESS_ID: address_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    address_does_not_exist = get_errors.ADDRESS_DOES_NOT_EXIST(id=address_id)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        address_does_not_exist.code: address_does_not_exist.render(),
      },
    })

  def test_get(self):
    address_value = 'value'
    address = Address.objects.create(is_active=True, value=address_value)

    payload = {
      get_constants.ADDRESS_ID: address._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [address],
    )
