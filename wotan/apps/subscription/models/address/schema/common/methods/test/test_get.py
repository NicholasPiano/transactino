
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from .....constants import address_fields
from ..... import Address
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

  def test_get_no_address(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    no_address = get_errors.NO_ADDRESS()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        no_address.code: no_address.render(),
      },
    })

  def test_get_with_input(self):
    payload = {
      'input': True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    address_get_takes_no_arguments = get_errors.ADDRESS_GET_TAKES_NO_ARGUMENTS()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        address_get_takes_no_arguments.code: address_get_takes_no_arguments.render(),
      },
    })

  def test_get(self):
    address_value = 'value'
    address = Address.objects.create(is_active=True, value=address_value)
    response = self.schema.respond(payload={}, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [address],
    )
