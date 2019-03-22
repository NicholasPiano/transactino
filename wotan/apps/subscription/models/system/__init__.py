
import uuid

from util.gpg import GPG

from django.db import models
from django.conf import settings

from apps.base.models import Model, Manager, model_fields

from ...constants import mode_constants, APP_LABEL

class SystemManager(Manager):
  def active(self):
    return self.get(is_active=True)

class System(Model):
  objects = SystemManager()

  public_key = models.TextField(default='')
  long_key_id = models.CharField(max_length=255, default='')
  is_active = models.BooleanField(default=True)

  class Meta:
    app_label = APP_LABEL

  def import_public_key(self):
    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    public_key_import = gpg.import_key(self.public_key)

    self.long_key_id = public_key_import.long_key_id
    self.save()
