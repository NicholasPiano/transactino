
import random

from django.db import models

from apps.base.models import Model, Manager

from ...constants import APP_LABEL, mode_constants
from .constants import address_constants, address_fields
from .schema.common import AddressModelSchema
from .schema.superadmin import AddressSuperadminModelSchema

class AddressManager(Manager):
  def get_active_address(self):
    return self.get(is_active=True)

  def attributes(self, mode=None):
    attributes = super().attributes(mode=mode)

    fields = [
      address_fields.VALUE,
    ]

    if mode == mode_constants.SUPERADMIN:
      fields.extend([
        address_fields.IS_ACTIVE,
        address_fields.IS_FLAGGED_FOR_SATURATION,
      ])

    return [
      attribute
      for attribute in attributes
      if attribute.name in fields
    ]

  def relationships(self, mode=None):
    if mode == mode_constants.SUPERADMIN:
      return super().relationships(mode=mode)

    return []

  def schema(self, mode=None):
    if mode == mode_constants.SUPERADMIN:
      return AddressSuperadminModelSchema(self.model, mode=mode)

    if mode != mode_constants.ANONYMOUS:
      return AddressModelSchema(self.model, mode=mode)

class Address(Model):
  objects = AddressManager()

  value = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_flagged_for_saturation = models.BooleanField(default=False)

  class Meta:
    app_label = APP_LABEL

  def get_open_unique_btc_amount(self):
    while True:
      random_btc_amount = random.randrange(address_constants.MAX_UNIQUE_BTC_AMOUNT)
      payment_exists_with_amount = self.payments_received.filter(
        is_open=False,
        has_been_used=True,
        unique_btc_amount=random_btc_amount,
      ).exists()

      if not payment_exists_with_amount:
        return random_btc_amount
