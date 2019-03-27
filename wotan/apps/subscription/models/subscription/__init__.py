
import uuid
import datetime

from django.apps import apps
from django.db import models
from django.utils import timezone
from django.conf import settings
scheduler = settings.SCHEDULER

from apps.base.models import Model, Manager, model_fields
from apps.base.schema.constants import schema_constants

from ...constants import mode_constants, APP_LABEL
from .constants import subscription_constants, subscription_fields
from .schema.common import SubscriptionModelSchema
from .schema.superadmin import SubscriptionSuperadminModelSchema

class SubscriptionManager(Manager):
  def attributes(self, mode=None):
    fields = [
      subscription_fields.ACTIVATION_DATE,
      subscription_fields.IS_VALID_UNTIL,
      subscription_fields.HAS_BEEN_ACTIVATED,
      subscription_fields.DURATION_IN_DAYS,
      subscription_fields.IS_ACTIVE,
      subscription_fields.ORIGIN,
    ]
    if mode == mode_constants.SUPERADMIN:
      fields.extend([
        subscription_fields.LAST_UPDATE_TIME,
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
      return SubscriptionSuperadminModelSchema(self.model, mode=mode)

    if mode != mode_constants.ANONYMOUS:
      return SubscriptionModelSchema(self.model, mode=mode)

class Subscription(Model):
  objects = SubscriptionManager()

  account = models.ForeignKey(
    subscription_constants.ACCOUNT_RELATED_MODEL,
    related_name=subscription_constants.ACCOUNT_RELATED_NAME,
    on_delete=models.CASCADE,
  )

  origin = models.UUIDField(default=uuid.uuid4)

  duration_in_days = models.PositiveIntegerField(default=0)
  activation_date = models.DateTimeField(auto_now_add=False, null=True)
  is_valid_until = models.DateTimeField(auto_now_add=False, null=True)

  has_been_activated = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  last_update_time = models.DateTimeField(auto_now_add=False, null=True)

  is_contract_signed = models.BooleanField(default=False)
  contract = models.TextField(default='')
  contract_client_signature = models.TextField(default='')
  contract_system_signature = models.TextField(default='')

  class Meta:
    app_label = APP_LABEL

  def get_btc_amount(self):
    return self.duration_in_days * subscription_constants.DEFAULT_COST_PER_DAY

  def activate(self):
    self.has_been_activated = True

    current_date = timezone.now()
    self.activation_date = self.activation_date if current_date < self.activation_date else current_date
    self.is_valid_until = self.activation_date + datetime.timedelta(days=self.duration_in_days)
    self.save()

  def update(self):
    if self.activation_date is not None:
      if self.has_been_activated and timezone.now() > self.activation_date:
        self.is_active = True

    if self.is_valid_until is not None:
      if timezone.now() > self.is_valid_until:
        self.is_active = False

    self.last_update_time = timezone.now()
    self.save()

def subscription_task():
  if scheduler is not None:
    for subscription in Subscription.objects.all():
      subscription.update()

if scheduler is not None:
  scheduler.add_job(
    subscription_task,
    trigger='interval',
    seconds=1,
    id=subscription_constants.SUBSCRIPTION_TASK,
    replace_existing=True,
  )
