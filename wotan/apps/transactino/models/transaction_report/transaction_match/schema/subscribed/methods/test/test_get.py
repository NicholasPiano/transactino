
import json
import uuid

from django.db import models
from django.test import TestCase
from django.conf import settings

from util.api.constants import constants

from apps.base.constants import model_fields
from apps.subscription.models import Account, Challenge

from ...... import TransactionReport
from ......constants import transaction_report_fields
from ..... import TransactionMatch
from .....constants import transaction_match_constants, transaction_match_fields
from ..constants import get_constants
from ..errors import get_errors
from ..get import TransactionMatchGetSchema

class TestContext():
  def __init__(self, account):
    self.account = account

  def get_account(self):
    return self.account

class TransactionMatchGetSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = TransactionMatchGetSchema(TransactionMatch)
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
    self.transaction_match_1_1 = self.transaction_report_1.matches.create(
      is_new=True,
      block_hash=self.block_hash_1,
    )
    self.transaction_match_1_2 = self.transaction_report_1.matches.create(
      is_new=False,
      block_hash=self.block_hash_2,
    )
    self.transaction_match_2_1 = self.transaction_report_2.matches.create(
      is_new=True,
      block_hash=self.block_hash_1,
    )
    self.transaction_match_2_2 = self.transaction_report_2.matches.create(
      is_new=False,
      block_hash=self.block_hash_2,
    )
    self.transaction_match_3_1 = self.transaction_report_3.matches.create(
      is_new=True,
      block_hash=self.block_hash_1,
    )
    self.transaction_match_3_2 = self.transaction_report_3.matches.create(
      is_new=False,
      block_hash=self.block_hash_2,
    )

  def test_get_does_not_exist(self):
    transaction_match_id = uuid.uuid4().hex

    payload = {
      get_constants.TRANSACTION_MATCH_ID: transaction_match_id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    transaction_match_does_not_exist = get_errors.TRANSACTION_MATCH_DOES_NOT_EXIST(id=transaction_match_id)
    self.assertEqual(
      response.render(),
      {
        constants.ERRORS: {
          transaction_match_does_not_exist.code: transaction_match_does_not_exist.render(),
        },
      },
    )

  def test_get(self):
    payload = {}

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.transaction_match_1_1,
        self.transaction_match_1_2,
        self.transaction_match_2_1,
        self.transaction_match_2_2,
        self.transaction_match_3_1,
        self.transaction_match_3_2,
      ]),
    )

  def test_get_id(self):
    payload = {
      get_constants.TRANSACTION_MATCH_ID: self.transaction_match_1_1._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(set(response.internal_queryset), set([self.transaction_match_1_1]))

  def test_get_transaction_report_id(self):
    payload = {
      get_constants.TRANSACTION_REPORT_ID: self.transaction_report_1._id,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.transaction_match_1_1,
        self.transaction_match_1_2,
      ]),
    )

  def test_get_transaction_report_target_address(self):
    payload = {
      get_constants.TRANSACTION_REPORT_TARGET_ADDRESS: self.target_address_1,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.transaction_match_1_1,
        self.transaction_match_1_2,
        self.transaction_match_2_1,
        self.transaction_match_2_2,
      ]),
    )

  def test_get_transaction_report_is_active(self):
    payload = {
      get_constants.TRANSACTION_REPORT_IS_ACTIVE: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.transaction_match_2_1,
        self.transaction_match_2_2,
        self.transaction_match_3_1,
        self.transaction_match_3_2,
      ]),
    )

  def test_get_is_new(self):
    payload = {
      transaction_match_fields.IS_NEW: True,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.transaction_match_1_1,
        self.transaction_match_2_1,
        self.transaction_match_3_1,
      ]),
    )

  def test_get_block_hash(self):
    payload = {
      transaction_match_fields.BLOCK_HASH: self.block_hash_2,
    }

    response = self.schema.respond(payload=payload, context=self.context)

    self.assertEqual(
      set(response.internal_queryset),
      set([
        self.transaction_match_1_2,
        self.transaction_match_2_2,
        self.transaction_match_3_2,
      ]),
    )
