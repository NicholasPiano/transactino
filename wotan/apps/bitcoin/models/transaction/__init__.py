
from django.db import models
from django.apps import apps
from django.conf import settings

from util.bitcoin import get_transaction

from apps.base.models import Model, Manager

from ...constants import APP_LABEL
from .constants import (
  transaction_prototype_constants, transaction_prototype_fields,
  transaction_constants, transaction_fields,
)

scheduler = settings.SCHEDULER

class TransactionPrototype(Model):
  txid = models.CharField(max_length=64)

  class Meta:
    app_label = APP_LABEL

class TransactionManager(Manager):
  def raw(self, transactions_json):
    raw_transactions = []
    for transaction_json in transactions_json:
      raw_transactions.append(self.model(transaction_json=transaction_json))

    return raw_transactions

class Transaction(Model):
  objects = TransactionManager()

  block = models.ForeignKey(
    transaction_constants.BLOCK_RELATED_MODEL,
    related_name=transaction_constants.BLOCK_RELATED_NAME,
    on_delete=models.CASCADE,
    null=True,
  )

  txid = models.CharField(max_length=64)
  hash = models.CharField(max_length=64)
  size = models.PositiveIntegerField(default=0)
  is_complete = models.BooleanField(default=False)

  class Meta:
    app_label = APP_LABEL

  def __init__(self, *args, transaction_json=None, **kwargs):
    super().__init__(*args, **kwargs)
    self.is_raw = False
    if transaction_json is not None:
      self.from_raw(transaction_json)

  def from_raw(self, transaction_json):
    self.is_raw = True
    self.txid = transaction_json.get('txid')
    self.hash = transaction_json.get('hash')
    self.size = transaction_json.get('size')

    self.raw_incoming_deltas = self.incoming_deltas.raw_incoming(transaction_json.get('vin'))
    self.raw_outgoing_deltas = self.outgoing_deltas.raw_outgoing(transaction_json.get('vout'))

  def is_ready(self, block, transaction_json):
    if self.is_complete:
      return True

    Delta = apps.get_model(APP_LABEL, 'Delta')

    is_vin_ready = True
    for vin_json in transaction_json.get('vin'):
      if 'coinbase' not in vin_json:
        if not Delta.objects.is_incoming_ready(self, vin_json):
          is_vin_ready = False

    is_vout_ready = True
    for vout_json in transaction_json.get('vout'):
      if not Delta.objects.is_outgoing_ready(self, vout_json):
        is_vout_ready = False

    is_ready = is_vin_ready and is_vout_ready
    if is_ready:
      self.hash = transaction_json.get('hash')
      self.size = int(transaction_json.get('size'))
      self.is_complete = True
      self.block = block
      self.save()

    return is_ready

  def get_fee(self):
    total_incoming = sum([
      delta.value
      for delta
      in (
        self.raw_incoming_deltas
        if self.is_raw
        else self.incoming_deltas.all()
      )
    ])

    total_outgoing = sum([
      delta.value
      for delta
      in (
        self.raw_outgoing_deltas
        if self.is_raw
        else self.outgoing_deltas.all()
      )
    ])

    if total_incoming:
      fee = total_incoming - total_outgoing
      density = fee / self.size if fee else 0

      return fee, density

    return 0, 0
