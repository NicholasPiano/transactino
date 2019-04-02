
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.base.constants import model_fields
from apps.subscription.models import Account

from ..... import TransactionMatch
from ..dismiss import TransactionMatchDismissSchema

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class TransactionMatchDismissSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = TransactionMatchDismissSchema(TransactionMatch)
    self.account = Account.objects.create(public_key=settings.TEST_PUBLIC_KEY)
    self.account.import_public_key()
    self.context = TestContext(self.account)
    self.block_hash_1 = 'block_hash_1'
    self.block_hash_2 = 'block_hash_2'
    self.target_address_1 = 'target_address_1'
    self.target_address_2 = 'target_address_2'
    self.transaction_report_1 = self.account.transaction_reports.create(
      target_address=self.target_address_1,
      is_active=False,
    )
    self.transaction_report_2 = self.account.transaction_reports.create(
      target_address=self.target_address_1,
      is_active=True,
    )
    self.transaction_report_3 = self.account.transaction_reports.create(
      target_address=self.target_address_2,
      is_active=True,
    )
    self.transaction_match_1 = self.transaction_report_1.matches.create(
      is_new=True,
      block_hash=self.block_hash_1,
    )
    self.transaction_match_2 = self.transaction_report_2.matches.create(
      is_new=True,
      block_hash=self.block_hash_1,
    )
    self.transaction_match_3 = self.transaction_report_3.matches.create(
      is_new=True,
      block_hash=self.block_hash_1,
    )

  def test_dismiss(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.transaction_match_1.refresh_from_db()
    self.assertFalse(self.transaction_match_1.is_new)

    self.transaction_match_2.refresh_from_db()
    self.assertFalse(self.transaction_match_2.is_new)

    self.transaction_match_3.refresh_from_db()
    self.assertFalse(self.transaction_match_3.is_new)

    self.assertFalse(response.internal_queryset)
