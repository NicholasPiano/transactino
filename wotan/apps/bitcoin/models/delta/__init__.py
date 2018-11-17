
from django.db import models
from django.conf import settings

from util.bitcoin import get_transaction

from apps.base.models import Model, Manager

from ...models import Address
from ...constants import APP_LABEL
from .constants import (
  delta_prototype_constants, delta_prototype_fields,
  delta_constants, delta_fields,
)

scheduler = settings.SCHEDULER

class DeltaPrototype(Model):
  txid = models.CharField(max_length=64)
  index = models.PositiveIntegerField(default=0)

  class Meta:
    app_label = APP_LABEL

class DeltaManager(Manager):
  def raw_incoming(self, vins_json):
    raw_vins = []
    for vin_json in vins_json:
      if 'coinbase' not in vin_json:
        raw_vins.append(self.model(vin_json=vin_json))

    return raw_vins

  def raw_outgoing(self, vouts_json):
    raw_vouts = []
    for vout_json in vouts_json:
      raw_vouts.append(self.model(vout_json=vout_json))

    return raw_vouts

  def is_incoming_ready(self, transaction, vin_json):
    txid = vin_json.get('txid')
    index = int(vin_json.get('vout'))

    delta = self.get(txid=txid, index=index)
    if delta is None:
      DeltaPrototype.objects.create(txid=txid, index=index)
      return False

    return delta.is_incoming_ready(transaction)

  def is_outgoing_ready(self, transaction, vout_json):
    index = int(vout_json.get('n'))

    delta = self.get(txid=transaction.txid, index=index)
    if delta is None:
      DeltaPrototype.objects.create(txid=transaction.txid, index=index)
      return False

    return delta.is_outgoing_ready(transaction, vout_json)

class Delta(Model):
  objects = DeltaManager()

  from_transaction = models.ForeignKey(
    delta_constants.FROM_TRANSACTION_RELATED_MODEL,
    related_name=delta_constants.FROM_TRANSACTION_RELATED_NAME,
    on_delete=models.CASCADE,
    null=True,
  )
  to_transaction = models.ForeignKey(
    delta_constants.TO_TRANSACTION_RELATED_MODEL,
    related_name=delta_constants.TO_TRANSACTION_RELATED_NAME,
    on_delete=models.CASCADE,
    null=True,
  )
  addresses = models.ManyToManyField(
    delta_constants.ADDRESSES_RELATED_MODEL,
    related_name=delta_constants.ADDRESSES_RELATED_NAME,
  )

  txid = models.CharField(max_length=64)
  value = models.BigIntegerField(default=0)
  index = models.PositiveIntegerField(default=0)
  is_complete = models.BooleanField(default=False)

  def __init__(self, *args, vin_json=None, vout_json=None, **kwargs):
    super().__init__(*args, **kwargs)
    if vin_json is not None:
      self.from_raw_incoming(vin_json)

    if vout_json is not None:
      self.from_raw_outgoing(vout_json)

  def from_raw_incoming(self, vin_json):
    self.txid = vin_json.get('txid')
    self.index = vin_json.get('vout')

    past_transaction_json = get_transaction(self.txid)
    past_vout = past_transaction_json.get('vout')[self.index]
    self.value = past_vout.get('value') * 10e8

  def from_raw_outgoing(self, vout_json):
    self.index = vout_json.get('n')
    self.value = vout_json.get('value') * 10e8
    self.raw_addresses = self.addresses.raw(vout_json.get('scriptPubKey').get('addresses'))

  def is_incoming_ready(self, transaction):
    self.to_transaction = transaction
    if self.from_transaction is not None:
      self.is_complete = True

    self.save()

    return True

  def is_outgoing_ready(self, transaction, vout_json):
    addresses = vout_json.get('scriptPubKey').get('addresses')

    is_ready = True
    if addresses is not None:
      for address_value in addresses:
        if not Address.objects.is_ready(address_value):
          is_ready = False

    if is_ready:
      self.value = int(float(vout_json.get('value')) * 1e8)

      if addresses is not None:
        for address_value in addresses:
          self.addresses.add(Address.objects.get(value=address_value))

      self.from_transaction = transaction
      if self.to_transaction is not None:
        self.is_complete = True

      self.save()

    return is_ready

  class Meta:
    app_label = APP_LABEL
