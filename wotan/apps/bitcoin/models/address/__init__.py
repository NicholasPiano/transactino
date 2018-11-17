
from django.db import models
from django.conf import settings
from django.utils import timezone

from apps.base.models import Model, Manager

from ...constants import APP_LABEL
from .constants import (
  address_prototype_constants, address_prototype_fields,
  address_constants, address_fields,
)

scheduler = settings.SCHEDULER

class AddressPrototype(Model):
  value = models.CharField(max_length=64)

  class Meta:
    app_label = APP_LABEL

class AddressManager(Manager):
  def raw(self, address_values):
    if address_values is None:
      return []

    return [
      self.model(address_value)
      for address_value
      in address_values
    ]

  def is_ready(self, value):
    address = self.get(value=value)
    if address is None:
      AddressPrototype.objects.create(value=value)
      return False

    return True

class Address(Model):
  objects = AddressManager()

  value = models.CharField(max_length=64, unique=True)

  class Meta:
    app_label = APP_LABEL
