
from django.db import models

from apps.base.models import Model, Manager
from apps.subscription.models import Account

from ....constants import APP_LABEL
from .constants import (
  transaction_match_constants,
)

class TransactionMatchManager(Manager):
  pass

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
