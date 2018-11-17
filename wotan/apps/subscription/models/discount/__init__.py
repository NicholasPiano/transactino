
from django.db import models

from apps.base.models import Model, Manager, model_fields

from ...constants import mode_constants, APP_LABEL
from .constants import discount_fields
from .schema import DiscountModelSchema

class DiscountManager(Manager):
  def consume(self, id=None):
    discount = self.get(id=id)
    if discount is None or not discount.is_open:
      return

    discount.is_open = False
    discount.save()
    
    return discount

  def schema(self, mode=None):
    if mode == mode_constants.SUPERADMIN:
      return DiscountModelSchema(self.model, mode=mode)

class Discount(Model):
  objects = DiscountManager()

  value = models.BigIntegerField(default=0)
  is_open = models.BooleanField(default=False)

  class Meta:
    app_label = APP_LABEL
