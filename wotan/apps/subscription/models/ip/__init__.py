
from django.db import models

from apps.base.models import Model, Manager, model_fields

from ...constants import mode_constants, APP_LABEL
from .constants import ip_constants, ip_fields
from .schema.subscribed import IPSubscribedModelSchema
from .schema.superadmin import IPSuperadminModelSchema

class IPManager(Manager):
  def attributes(self, mode=None):
    fields = [
      ip_fields.VALUE,
      ip_fields.IS_ONLINE,
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
    if mode == mode_constants.SUBSCRIBED:
      return IPSubscribedModelSchema(self.model, mode=mode)

    if mode == mode_constants.SUPERADMIN:
      return IPSuperadminModelSchema(self.model, mode=mode)

class IP(Model):
  objects = IPManager()

  account = models.ForeignKey(
    ip_constants.ACCOUNT_RELATED_MODEL,
    related_name=ip_constants.ACCOUNT_RELATED_NAME,
    on_delete=models.CASCADE,
  )

  value = models.CharField(max_length=255)
  is_online = models.BooleanField(default=False)

  class Meta:
    app_label = APP_LABEL

  def bring_online(self):
    self.is_online = True
    self.save()
    self.account.bring_online()

  def take_offline(self):
    if self.connections.get(is_online=True) is None:
      self.is_online = False
      self.save()
      self.account.take_offline()
