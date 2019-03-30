
import uuid

from util.gpg import GPG

from django.db import models
from django.utils import timezone
from django.conf import settings

from apps.base.models import Model, Manager, model_fields
from apps.base.schema.constants import schema_constants

from ...constants import mode_constants, APP_LABEL
from .constants import announcement_constants, announcement_fields
from .schema.common import AnnouncementModelSchema

class AnnouncementManager(Manager):
  def create_and_sign(self, *args, **kwargs):
    created = super().create(*args, **kwargs)
    created.sign_matter()

    return created

  def active(self):
    return self.filter(system__is_active=True, is_active=True)

  def attributes(self, mode=None):
    fields = [
      announcement_fields.MATTER,
      announcement_fields.SIGNATURE,
      announcement_fields.DATE_ACTIVATED,
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
    return {
      schema_constants.ATTRIBUTES: self.serialize_attributes(
        instance,
        attributes=attributes,
        mode=mode,
      ),
    }

  def schema(self, mode=None):
    if mode != mode_constants.SUPERADMIN:
      return AnnouncementModelSchema(self.model, mode=mode)

class Announcement(Model):
  objects = AnnouncementManager()

  system = models.ForeignKey(
    announcement_constants.SYSTEM_RELATED_MODEL,
    related_name=announcement_constants.SYSTEM_RELATED_NAME,
    on_delete=models.CASCADE,
  )

  matter = models.TextField(
    default='',
    verbose_name='The main body of the announcement',
  )
  signature = models.TextField(
    default='',
    verbose_name='The signature of the system for this announcement',
  )
  is_active = models.BooleanField(default=False)
  date_activated = models.DateTimeField(null=True)

  class Meta:
    app_label = APP_LABEL

  def sign_matter(self):
    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    self.signature = gpg.sign_with_private(self.matter)
    self.save()

  def activate(self):
    self.is_active = True
    self.date_activated = timezone.now()
    self.save()
