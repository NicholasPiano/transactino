
import random

from django.db import models

from apps.base.models import Model, Manager

from ...constants import APP_LABEL, mode_constants
from .constants import address_constants, address_fields
from .schema.common import AddressModelSchema

class AddressManager(Manager):
  def get_active_address(self):
    return self.get(is_external=False, is_active=True)

  def schema(self, mode=None):
    if mode == mode_constants.SUPERADMIN:
      return AddressModelSchema(self.model, mode=mode)

class Address(Model):
  objects = AddressManager()

  value = models.CharField(max_length=255)
  is_external = models.BooleanField(default=True)
  is_active = models.BooleanField(default=True)

  class Meta:
    app_label = APP_LABEL

  def get_open_unique_btc_amount(self):
    while True:
      random_btc_amount = random.randrange(address_constants.MAX_UNIQUE_BTC_AMOUNT)
      if not self.payments_received.filter(is_open=False, has_been_used=True, unique_btc_amount=random_btc_amount).exists():
        return random_btc_amount
