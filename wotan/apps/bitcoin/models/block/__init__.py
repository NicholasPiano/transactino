
import json

from django.apps import apps
from django.db import models
from django.conf import settings
from django.utils import timezone

from util.bitcoin import get_info, get_block, get_transaction

from apps.base.models import Model, Manager

from ...constants import APP_LABEL
from .constants import (
  block_prototype_constants, block_prototype_fields,
  block_constants, block_fields,
)

scheduler = settings.SCHEDULER

class BlockPrototype(Model):
  hash = models.CharField(max_length=64)

  class Meta:
    app_label = APP_LABEL

class BlockManager(Manager):
  def is_ready(self, hash):
    block = self.get(hash=hash)
    if block is None:
      BlockPrototype.objects.create(hash=hash)

    return True

  def raw(self, hash):
    return self.model(block_json=get_block(hash))

  def get_previous_hash(self, hash):
    return get_block(hash).get('previousblockhash')

class Block(Model):
  objects = BlockManager()

  parent = models.CharField(max_length=64)
  height = models.PositiveIntegerField(default=0)
  hash = models.CharField(max_length=64, unique=True)
  start_time = models.DateTimeField(auto_now_add=True)
  end_time = models.DateTimeField(null=True)
  is_complete = models.BooleanField(default=False)

  class Meta:
    app_label = APP_LABEL

  def __init__(self, *args, block_json=None, **kwargs):
    super().__init__(*args, **kwargs)
    if block_json is not None:
      self.from_raw(block_json)

  def from_raw(self, block_json):
    self.parent = block_json.get('previousblockhash')
    self.height = block_json.get('height')
    self.hash = block_json.get('hash')
    self.raw_transactions = self.transactions.raw(block_json.get('tx'))
