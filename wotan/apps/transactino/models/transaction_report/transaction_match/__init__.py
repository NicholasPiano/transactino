
from django.db import models

from apps.base.models import Model, Manager
from apps.subscription.models import Account

from ....constants import APP_LABEL
from .constants import (
  transaction_match_constants,
  transaction_match_fields,
)
from .schema.subscribed import TransactionMatchSubscribedModelSchema

class TransactionMatchManager(Manager):
  def attributes(self, mode=None):
    fields = [
      transaction_match_fields.BLOCK_HASH,
      transaction_match_fields.TXID,
      transaction_match_fields.INDEX,
      transaction_match_fields.VALUE,
      transaction_match_fields.IS_NEW,
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

  def relationships(self, mode=None):
    fields = [
      transaction_match_fields.TRANSACTION_REPORT,
    ]

    return [
      field
      for field in self.model._meta.get_fields()
      if (
        field.is_relation
        or (
          field.auto_created
          and not field.concrete
        )
      )
    ]

  def schema(self, mode=None):
    if mode == mode_constants.SUBSCRIBED:
      return TransactionMatchSubscribedModelSchema(self.model, mode=mode)

class TransactionMatch(Model):
  objects = TransactionMatchManager()

  transaction_report = models.ForeignKey(
    transaction_match_constants.TRANSACTION_REPORT_RELATED_MODEL,
    related_name=transaction_match_constants.TRANSACTION_REPORT_RELATED_NAME,
    on_delete=models.CASCADE,
  )

  block_hash = models.CharField(max_length=64)
  txid = models.CharField(max_length=64)
  index = models.PositiveIntegerField(default=0)
  value = models.PositiveIntegerField(default=0)
  is_new = models.BooleanField(default=True)

  class Meta:
    app_label = APP_LABEL
