
import logging
logger = logging.getLogger('django.debug')

from django.db import models
from django.utils import timezone
from django.conf import settings
scheduler = settings.SCHEDULER

from util.bitcoin import get_latest_block_hash, get_previous_hash, Block

from apps.base.constants import model_fields
from apps.base.schema.constants import schema_constants
from apps.base.models import Model, Manager
from apps.subscription.constants import mode_constants
from apps.subscription.models import Account

from ...constants import APP_LABEL
from .constants import (
  fee_report_block_wrapper_prototype_constants, fee_report_block_wrapper_prototype_fields,
  fee_report_block_wrapper_constants, fee_report_block_wrapper_fields,
  fee_report_constants, fee_report_fields,
)
from .schema.subscribed import FeeReportSubscribedModelSchema
from .schema.superadmin import FeeReportSuperadminModelSchema

class FeeReportBlockWrapperPrototype(Model):
  hash = models.CharField(max_length=64)

  class Meta:
    app_label = APP_LABEL

class FeeReportBlockWrapperManager(Manager):
  def is_ready(self, hash):
    block_wrapper = self.get(hash=hash)
    if block_wrapper is None:
      FeeReportBlockWrapperPrototype.objects.create(hash=hash)
      return False

    return block_wrapper.is_ready()

class FeeReportBlockWrapper(Model):
  objects = FeeReportBlockWrapperManager()

  hash = models.CharField(max_length=64)
  average_tx_fee = models.FloatField(default=0.0)
  average_tx_fee_density = models.FloatField(default=0.0)
  start_time = models.DateTimeField(auto_now_add=True)
  end_time = models.DateTimeField(null=True)
  is_processing = models.BooleanField(default=False)
  is_complete = models.BooleanField(default=False)

  class Meta:
    app_label = APP_LABEL

  def is_ready(self):
    if self.is_complete:
      return True

    if self.is_processing:
      return False

    self.is_processing = True
    self.start_time = timezone.now()
    self.save()

    block = Block(self.hash)

    fees = []
    densities = []
    for transaction in block.transactions:
      fee, density = transaction.get_fee()
      if fee:
        fees.append(fee)
        densities.append(density)

    self.average_tx_fee = (sum(fees) / len(fees)) if fees else 0
    self.average_tx_fee_density = (sum(densities) / len(densities)) if fees else 0
    self.end_time = timezone.now()
    self.is_processing = False
    self.is_complete = True
    self.save()

def fee_report_block_wrapper_task():
  if scheduler is not None:
    FeeReportBlockWrapper.objects.bulk_create([
      FeeReportBlockWrapper(hash=prototype.hash)
      for prototype
      in FeeReportBlockWrapperPrototype.objects.all().distinct(
        fee_report_block_wrapper_prototype_fields.HASH,
      )
    ])
    FeeReportBlockWrapperPrototype.objects.all().delete()

if scheduler is not None:
  scheduler.add_job(
    fee_report_block_wrapper_task,
    trigger='interval',
    seconds=10,
    id=fee_report_block_wrapper_constants.FEE_REPORT_BLOCK_WRAPPER_TASK,
    replace_existing=True,
  )

class FeeReportManager(Manager):
  def attributes(self, mode=None):
    fields = [
      fee_report_fields.IS_ACTIVE,
      fee_report_fields.BLOCKS_TO_INCLUDE,
      fee_report_fields.AVERAGE_TX_FEE,
      fee_report_fields.AVERAGE_TX_FEE_DENSITY,
      fee_report_fields.LAST_UPDATE_END_TIME,
      fee_report_fields.LATEST_BLOCK_HASH,
    ]
    if mode == mode_constants.SUPERADMIN:
      fields.extend([
        fee_report_fields.LAST_UPDATE_START_TIME,
        fee_report_fields.HAS_BEEN_RUN,
        fee_report_fields.HAS_BEEN_READY,
      ])

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
    if mode == mode_constants.SUPERADMIN:
      return FeeReportSuperadminModelSchema(self.model, mode=mode)

    if mode == mode_constants.SUBSCRIBED:
      return FeeReportSubscribedModelSchema(self.model, mode=mode)

class FeeReport(Model):
  objects = FeeReportManager()

  account = models.ForeignKey(
    fee_report_constants.ACCOUNT_RELATED_MODEL,
    related_name=fee_report_constants.ACCOUNT_RELATED_NAME,
    on_delete=models.CASCADE,
  )

  is_active = models.BooleanField(default=False)
  blocks_to_include = models.PositiveIntegerField(default=1)

  latest_block_hash = models.CharField(max_length=64, default='')
  has_been_ready = models.BooleanField(default=False)
  has_been_run = models.BooleanField(default=False)
  is_processing = models.BooleanField(default=False)
  average_tx_fee = models.FloatField(default=0)
  average_tx_fee_density = models.FloatField(default=0)
  last_update_start_time = models.DateTimeField(auto_now_add=False, null=True)
  last_update_end_time = models.DateTimeField(auto_now_add=False, null=True)

  class Meta:
    app_label = APP_LABEL

  def process(self, latest_block_hash=None):
    if latest_block_hash is not None:
      if self.latest_block_hash != latest_block_hash:
        self.latest_block_hash = latest_block_hash
        self.last_update_start_time = timezone.now()
        self.save()

      if self.is_ready():
        self.run()

      self.save()

  def is_ready(self):
    is_ready = True
    active_block_hash = self.latest_block_hash

    block_count = 0
    while block_count < self.blocks_to_include:
      if not FeeReportBlockWrapper.objects.is_ready(hash=active_block_hash):
        is_ready = False

      active_block_hash = get_previous_hash(active_block_hash)
      block_count += 1

    return is_ready

  def run(self):
    fees = []
    densities = []
    active_block_hash = self.latest_block_hash

    for index_to_add in range(self.blocks_to_include):
      block_wrapper = FeeReportBlockWrapper.objects.get(hash=active_block_hash)
      fees.append(block_wrapper.average_tx_fee)
      densities.append(block_wrapper.average_tx_fee_density)

      active_block_hash = get_previous_hash(active_block_hash)

    self.average_tx_fee = (sum(fees) / len(fees)) if fees else 0
    self.average_tx_fee_density = (sum(densities) / len(densities)) if densities else 0
    self.last_update_end_time = timezone.now()
    self.has_been_run = True
    self.save()

def fee_report_task():
  if scheduler is not None:
    latest_block_hash = get_latest_block_hash()

    fee_reports = FeeReport.objects.filter(is_active=True)

    for fee_report in fee_reports:
      fee_report.process(latest_block_hash=latest_block_hash)

if scheduler is not None:
  scheduler.add_job(
    fee_report_task,
    trigger='interval',
    seconds=10,
    id=fee_report_constants.FEE_REPORT_TASK,
    replace_existing=True,
  )
