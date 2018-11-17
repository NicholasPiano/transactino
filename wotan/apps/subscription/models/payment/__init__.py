
import uuid

from django.utils import timezone
from django.db import models
from django.conf import settings
scheduler = settings.SCHEDULER

from relay.constants import relay_constants
from relay.send import send

from apps.base.models import Model, Manager, model_fields
from apps.base.schema.constants import schema_constants
from apps.bitcoin.models import Delta

from ...constants import mode_constants, APP_LABEL
from ..address import Address
from .constants import payment_constants, payment_fields
from .schema.common import PaymentModelSchema
from .schema.superadmin import PaymentSuperadminModelSchema

class PaymentManager(Manager):
  def attributes(self, mode=None):
    fields = [
      payment_fields.ADDRESS,
      payment_fields.FULL_BTC_AMOUNT,
    ]
    if mode == mode_constants.SUPERADMIN:
      fields.extend([
        payment_fields.ORIGIN,
        payment_fields.IS_OPEN,
        payment_fields.HAS_BEEN_USED,
        payment_fields.BASE_AMOUNT,
        payment_fields.UNIQUE_BTC_AMOUNT,
        payment_fields.TIME_CONFIRMED,
        payment_fields.BLOCK_HASH,
        payment_fields.TX_HASH,
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
  to_address = models.ForeignKey(
    payment_constants.TO_ADDRESS_RELATED_MODEL,
    related_name=payment_constants.TO_ADDRESS_RELATED_NAME,
    on_delete=models.CASCADE,
    null=True,
  )
  from_address = models.ForeignKey(
    payment_constants.FROM_ADDRESS_RELATED_MODEL,
    related_name=payment_constants.FROM_ADDRESS_RELATED_NAME,
    on_delete=models.CASCADE,
    null=True,
  )

  address = models.CharField(max_length=255, default='')
  origin = models.UUIDField(default=uuid.uuid4)

  is_open = models.BooleanField(default=True)
  has_been_used = models.BooleanField(default=False)
  time_confirmed = models.DateTimeField(auto_now_add=False, null=True)

  base_amount = models.BigIntegerField(default=0)
  unique_btc_amount = models.BigIntegerField(default=0)
  full_btc_amount = models.BigIntegerField(default=0)

  block_hash = models.CharField(max_length=64, default='')
  txid = models.CharField(max_length=64, default='')

  class Meta:
    app_label = APP_LABEL

  def update(self):
    active_address = Address.objects.get_active_address()
    delta = Delta.objects.get(
      addresses__value=active_address.value,
      value=self.full_btc_amount,
    )

    if delta is not None:
      self.is_open = False
      self.has_been_used = True
      self.time_confirmed = timezone.now()
      self.block_hash = delta.to_transaction.block.hash
      self.txid = delta.to_transaction.txid
      self.save()

  def prepare(self):
    if self.to_address is not None:
      self.unique_btc_amount = self.to_address.get_open_unique_btc_amount()
      self.full_btc_amount = self.base_amount + self.unique_btc_amount
      self.save()

def payment_task():
  if scheduler is not None:
    open_payments = Payment.objects.filter(is_open=True)

    for payment in open_payments:
      payment.update()

      if not payment.is_open:
        send(
          payment.account.active_channel,
          relay_constants.PAYMENT,
          payment,
        )

if scheduler is not None:
  scheduler.add_job(
    payment_task,
    trigger='interval',
    minutes=5,
    id=payment_constants.PAYMENT_TASK,
    replace_existing=True,
  )
