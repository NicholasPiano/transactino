
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from .......schema.with_challenge import with_challenge_constants, with_challenge_errors
from ......account import Account
from ......challenge import Challenge
from ..... import IP
from ..get import IPGetSchema
from ..constants import get_constants
from ..errors import get_errors

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class IPGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = IPGetSchema(IP)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)

  def test_get(self):
    ip = self.account.ips.create(value='ip-address')

    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    challenge = Challenge.objects.get(origin=get_constants.ORIGIN)

    challenge.is_open = False
    challenge.save()

    second_response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      list(second_response.internal_queryset),
      [ip],
    )

  def test_get_with_arguments(self):
    payload = {
      'key': 'value',
    }

    response = self.schema.respond(payload=payload, context=self.context)

    ip_get_takes_no_arguments = get_errors.IP_GET_TAKES_NO_ARGUMENTS()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        ip_get_takes_no_arguments.code: ip_get_takes_no_arguments.render(),
      },
    })
