
import uuid

from util.gpg import GPG

from django.db import models
from django.conf import settings

from apps.base.models import Model, Manager, model_fields
from apps.base.schema.constants import schema_constants

from ...constants import mode_constants, APP_LABEL
from .constants import system_fields
from .schema.common import SystemModelSchema

class SystemManager(Manager):
  def create_and_import(self, *args, **kwargs):
    created = super().create(*args, **kwargs)
    created.import_keys()

    return created

  def active(self):
    return self.get(is_active=True)

  def attributes(self, mode=None):
    fields = [
      system_fields.PUBLIC_KEY,
      system_fields.GUARANTEE,
      system_fields.GUARANTEE_SIGNATURE,
      system_fields.DISCLAIMER,
      system_fields.DISCLAIMER_SIGNATURE,
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
      return SystemModelSchema(self.model, mode=mode)

class System(Model):
  objects = SystemManager()

  private_key = models.TextField(
    default='',
    verbose_name='The GPG private key of the system',
  )
  public_key = models.TextField(
    default='',
    verbose_name='The GPG public key of the system',
  )
  long_key_id = models.CharField(
    max_length=255,
    default='',
    verbose_name='The GPG long key id corresponding to the public key',
  )
  guarantee = models.TextField(
    default='',
    verbose_name='The Transactino guarantee',
  )
  guarantee_signature = models.TextField(
    default='',
    verbose_name='The guarantee signature',
  )
  disclaimer = models.TextField(
    default='',
    verbose_name='The disclaimer',
  )
  disclaimer_signature = models.TextField(
    default='',
    verbose_name='The disclaimer signature',
  )
  is_active = models.BooleanField(default=True)

  class Meta:
    app_label = APP_LABEL

  def import_keys(self):
    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    private_key_import = gpg.import_key(self.private_key)
    public_key_import = gpg.import_key(self.public_key)

    self.long_key_id = public_key_import.long_key_id
    self.save()
