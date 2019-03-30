
import json

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from ......account import Account
from ......system import System
from .....constants import announcement_fields
from ..... import Announcement
from ..errors import get_errors
from ..get import AnnouncementGetSchema

class TestContext():
  def __init__(self, account=None):
    self.account = account

  def get_account(self):
    return self.account

class AnnouncementGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = AnnouncementGetSchema(Announcement)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(account=self.account)

  def test_get_with_input(self):
    payload = {
      'input': True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    announcement_get_takes_no_arguments = get_errors.ANNOUNCEMENT_GET_TAKES_NO_ARGUMENTS()
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        announcement_get_takes_no_arguments.code: announcement_get_takes_no_arguments.render(),
      },
    })

  def test_get(self):
    system = System.objects.create(is_active=True, public_key=settings.TEST_SYSTEM_PUBLIC_KEY)
    announcement = Announcement.objects.create(system=system, matter='matter', is_active=True)
    response = self.schema.respond(payload={}, context=self.context)

    self.assertEqual(
      list(response.internal_queryset),
      [announcement],
    )
