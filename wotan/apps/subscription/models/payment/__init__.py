
import uuid

from django.utils import timezone
from django.db import models
from django.conf import settings
scheduler = settings.SCHEDULER

from apps.base.models import Model, Manager, model_fields
from apps.base.schema.constants import schema_constants

from ...constants import mode_constants, APP_LABEL
from .constants import payment_constants, payment_fields
from .schema.common import PaymentModelSchema
from .schema.superadmin import PaymentSuperadminModelSchema
from .backend import WithPaymentCheck

class PaymentManager(Manager, WithPaymentCheck):
  def attributes(self, mode=None):
    attributes = super().attributes(mode=mode)

    fields = [
      payment_fields.FULL_BTC_AMOUNT,
      payment_fields.ORIGIN,
      payment_fields.IS_OPEN,
      payment_fields.TIME_CONFIRMED,
      payment_fields.BLOCK_HASH,
      payment_fields.TXID,
      payment_fields.INDEX,
    ]

    if mode == mode_constants.SUPERADMIN:
      fields.extend([
        payment_fields.HAS_BEEN_USED,
        payment_fields.BASE_AMOUNT,
        payment_fields.UNIQUE_BTC_AMOUNT,
      ])

    return [
      attribute
      for attribute in attributes
      if attribute.name in fields
    ]

  def relationships(self, mode=None):
    relationships = super().relationships(mode=mode)

    fields = [
      payment_fields.ADDRESS,
    ]

    if mode == mode_constants.SUPERADMIN:
      fields.extend([
        payment_fields.ACCOUNT,
      ])

    return [
      relationship
      for relationship in relationships
      if relationship.name in fields
    ]

  def schema(self, mode=None):
    if mode == mode_constants.SUPERADMIN:
      return PaymentSuperadminModelSchema(self.model, mode=mode)

    if mode != mode_constants.ANONYMOUS:
      return PaymentModelSchema(self.model, mode=mode)

class Payment(Model):
  objects = PaymentManager()

  account = models.ForeignKey(
    payment_constants.ACCOUNT_RELATED_MODEL,
    related_name=payment_constants.ACCOUNT_RELATED_NAME,
    on_delete=models.CASCADE,
  )
  address = models.ForeignKey(
    payment_constants.ADDRESS_RELATED_MODEL,
    related_name=payment_constants.ADDRESS_RELATED_NAME,
    on_delete=models.CASCADE,
    null=True,
  )

  origin = models.UUIDField(default=uuid.uuid4)

  is_open = models.BooleanField(default=True)
  has_been_used = models.BooleanField(default=False)
  time_confirmed = models.DateTimeField(auto_now_add=False, null=True)

  base_amount = models.BigIntegerField(default=0)
  unique_btc_amount = models.BigIntegerField(default=0)
  full_btc_amount = models.BigIntegerField(default=0)

  block_hash = models.CharField(max_length=64, default='')
  txid = models.CharField(max_length=64, default='')
  index = models.PositiveIntegerField(default=0)

  class Meta:
    app_label = APP_LABEL

  def close(self, block_hash, txid, index):
    self.is_open = False
    self.time_confirmed = timezone.now()
    self.block_hash = block_hash
    self.txid = txid
    self.index = index
    self.save()

  def prepare(self):
    if self.address is not None:
      self.unique_btc_amount = self.address.get_open_unique_btc_amount()
      self.full_btc_amount = self.base_amount + self.unique_btc_amount
      self.save()

def payment_task():
  if scheduler is not None:
    Payment.objects.check_payments()

if scheduler is not None:
  scheduler.add_job(
    payment_task,
    trigger='interval',
    seconds=120,
    id=payment_constants.PAYMENT_TASK,
    replace_existing=True,
  )
