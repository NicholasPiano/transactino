
from django.db import models
from django.utils import timezone
from django.conf import settings
scheduler = settings.SCHEDULER

from util.blockchaininfo import get_latest_block_hash, get_previous_hash, Block

from apps.base.constants import model_fields
from apps.base.schema.constants import schema_constants
from apps.base.models import Model, Manager
from apps.subscription.constants import mode_constants
from apps.subscription.models import Account

from ...constants import APP_LABEL
from .constants import (
  transaction_report_constants,
  transaction_report_fields,
)
from .schema.subscribed import TransactionReportSubscribedModelSchema

class TransactionReportManager(Manager):
  def attributes(self, mode=None):
    fields = [
      transaction_report_fields.IS_ACTIVE,
      transaction_report_fields.TARGET_ADDRESS,
      transaction_report_fields.VALUE_EQUAL_TO,
      transaction_report_fields.VALUE_GREATER_THAN,
      transaction_report_fields.VALUE_LESS_THAN,
      transaction_report_fields.LATEST_BLOCK_HASH,
    ]

    return [
      field
      for field in self.model._meta.get_fields()
      if (
        not field.is_relation
        and field.name != model_fields.ID
        and field.name in fields
      )
    ]

  def serialize(self, instance, attributes=None, relationships=None, mode=None):
    serialized = {
      schema_constants.ATTRIBUTES: self.serialize_attributes(
        instance,
        attributes=attributes,
        mode=mode,
      ),
    }

    if mode == mode_constants.SUPERADMIN:
      serialized.update({
        schema_constants.RELATIONSHIPS: self.serialize_relationships(
          instance,
          relationships=relationships,
          mode=mode,
        ),
      })

    return serialized

  def schema(self, mode=None):
    if mode == mode_constants.SUBSCRIBED:
      return TransactionReportSubscribedModelSchema(self.model, mode=mode)

class TransactionReport(Model):
  objects = TransactionReportManager()

  account = models.ForeignKey(
    transaction_report_constants.ACCOUNT_RELATED_MODEL,
    related_name=transaction_report_constants.ACCOUNT_RELATED_NAME,
    on_delete=models.CASCADE,
  )

  is_active = models.BooleanField(default=False)
  target_address = models.CharField(max_length=255)
  value_equal_to = models.PositiveIntegerField(null=True)
  value_greater_than = models.PositiveIntegerField(default=0)
  value_less_than = models.PositiveIntegerField(null=True)
  latest_block_hash = models.CharField(max_length=64, default='')
  last_update_time = models.DateTimeField(auto_now_add=False, null=True)

  class Meta:
    app_label = APP_LABEL

  def match(self, value):
    if self.value_equal_to is not None:
      if value == self.value_equal_to:
        return True

      return False

    greater_than = value > self.value_greater_than

    if self.value_less_than is None:
      return greater_than

    less_than = value < self.value_less_than

    return greater_than and less_than

  def process(self, block):
    if block.hash is None or block.hash == self.latest_block_hash:
      return

    self.latest_block_hash = block.hash
    deltas = block.find_deltas_with_address(self.target_address)

    for delta in deltas:
      if self.match(delta.value):
        self.matches.create(
          block_hash=block.hash,
          txid=delta.out_txid,
          index=delta.index,
          value=delta.value,
        )

def transaction_report_task():
  if scheduler is not None:
    # latest_block_hash = get_latest_block_hash()
    block = Block('0000000000000000000218ee3e7ed66c0c4344cd03b97dfac84c5546f66e7b88')
    if block.has_failed:
      return

    transaction_reports = TransactionReport.objects.filter(is_active=True)

    for transaction_report in transaction_reports:
      transaction_report.process(block)

if scheduler is not None:
  scheduler.add_job(
    transaction_report_task,
    trigger='interval',
    seconds=120,
    id=transaction_report_constants.TRANSACTION_REPORT_TASK,
    replace_existing=True,
  )
