
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......system import System
from ..... import Account
from .....constants import account_fields
from ..constants import create_constants
from ..errors import account_anonymous_method_errors
from ..create import (
  AccountCreatePublicKeyResponse,
  AccountCreatePublicKeySchema,
  AccountCreateSchema,
)

class AccountCreatePublicKeyResponseTestCase(TestCase):
  def setUp(self):
    self.schema = AccountCreatePublicKeySchema()
    self.response = self.schema.get_response()

  def test_long_key_id(self):
    long_key_id = 'long_key_id'
    self.response.set_long_key_id(long_key_id)
    self.assertEqual(self.response.get_long_key_id(), long_key_id)

class AccountCreatePublicKeySchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AccountCreatePublicKeySchema()

  def test_valid_public_key(self):
    payload = settings.TEST_PUBLIC_KEY

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.render(), payload)

  def test_invalid_public_key(self):
    payload = 'xxx'

    response = self.schema.respond(payload=payload)

    invalid_public_key = account_anonymous_method_errors.INVALID_PUBLIC_KEY()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        invalid_public_key.code: invalid_public_key.render(),
      },
    })

class TestContext():
  class connection:
    ip_value = 'ip_value'

    def save():
      pass

  def update_from_connection(self):
    pass

class TestContext2():
  class connection:
    ip_value = 'ip_value2'

    def save():
      pass

  def update_from_connection(self):
    pass

class AccountCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AccountCreateSchema(Account)
    self.system = System.objects.create_and_import(
      public_key=settings.TEST_SYSTEM_PUBLIC_KEY,
      private_key=settings.TEST_SYSTEM_PRIVATE_KEY,
    )
    self.public_key = settings.TEST_PUBLIC_KEY

  def test_create_no_public_key(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=TestContext())

    self.assertFalse(Account.objects.all())

    public_key_not_included = account_anonymous_method_errors.PUBLIC_KEY_NOT_INCLUDED()

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        public_key_not_included.code: public_key_not_included.render(),
      },
    })

  def test_create_valid_public_key(self):
    payload = {
      account_fields.PUBLIC_KEY: self.public_key,
    }

    response = self.schema.respond(payload=payload, context=TestContext())

    account = Account.objects.get()
    self.assertEqual(account.public_key, self.public_key)
    self.assertEqual(
      response.render(),
      {
        create_constants.DISCLAIMER: self.system.disclaimer,
        create_constants.IP: TestContext().connection.ip_value,
        create_constants.LONG_KEY_ID: account.long_key_id,
      },
    )

  def test_create_valid_public_key_already_exists(self):
    payload = {
      account_fields.PUBLIC_KEY: self.public_key,
    }

    first_response = self.schema.respond(payload=payload, context=TestContext())

    self.assertEqual(Account.objects.count(), 1)
    self.assertEqual(Account.objects.get().public_key, self.public_key)

    second_response = self.schema.respond(payload=payload, context=TestContext2())

    account_already_exists = account_anonymous_method_errors.ACCOUNT_ALREADY_EXISTS()

    self.assertEqual(second_response.render(), {
      constants.ERRORS: {
        account_already_exists.code: account_already_exists.render(),
      },
    })

  def test_create_valid_public_key_ip_already_exists(self):
    payload = {
      account_fields.PUBLIC_KEY: self.public_key,
    }

    first_response = self.schema.respond(payload=payload, context=TestContext())

    self.assertEqual(Account.objects.count(), 1)
    self.assertEqual(Account.objects.get().public_key, self.public_key)

    second_response = self.schema.respond(payload=payload, context=TestContext())

    ip_already_exists = account_anonymous_method_errors.IP_ALREADY_EXISTS(TestContext().connection.ip_value)

    self.assertEqual(second_response.render(), {
      constants.ERRORS: {
        ip_already_exists.code: ip_already_exists.render(),
      },
    })
