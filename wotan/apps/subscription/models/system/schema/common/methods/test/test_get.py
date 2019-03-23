
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from .....constants import system_fields
from ..... import System
from ..errors import get_errors
from ..get import SystemGetSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

  def get_account(self):
    return self.account

class SystemGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = SystemGetSchema(System)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(account=self.account)

  def test_get_no_system(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    no_system = get_errors.NO_SYSTEM()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        no_system.code: no_system.render(),
      },
    })

  def test_get_with_input(self):
    payload = {
      'input': True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    system_get_takes_no_arguments = get_errors.SYSTEM_GET_TAKES_NO_ARGUMENTS()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        system_get_takes_no_arguments.code: system_get_takes_no_arguments.render(),
      },
    })

  def test_get(self):
    system = System.objects.create(is_active=True, public_key=settings.TEST_SYSTEM_PUBLIC_KEY)
    response = self.schema.respond(payload={}, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [system],
    )
