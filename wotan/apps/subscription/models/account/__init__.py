
from django.db import models
from django.conf import settings

from util.gpg import GPG

from apps.base.models import Model, Manager

from ...constants import mode_constants, APP_LABEL
from .constants import account_constants, account_fields
from .schema.anonymous import AccountAnonymousModelSchema
from .schema.unsubscribed import AccountUnsubscribedModelSchema
from .schema.subscribed import AccountSubscribedModelSchema
from .schema.superadmin import AccountSuperadminModelSchema

class AccountManager(Manager):
  def schema(self, mode=None):
    if mode == mode_constants.ANONYMOUS:
      return AccountAnonymousModelSchema(self.model)

    if mode == mode_constants.UNSUBSCRIBED:
      return AccountUnsubscribedModelSchema(self.model)

    if mode == mode_constants.SUBSCRIBED:
      return AccountSubscribedModelSchema(self.model)

    if mode == mode_constants.SUPERADMIN:
      return AccountSuperadminModelSchema(self.model)

class Account(Model):
  objects = AccountManager()

  public_key = models.TextField(default='', verbose_name='')
  long_key_id = models.CharField(max_length=255, default='')
  is_superadmin = models.BooleanField(default=False)
  is_verified = models.BooleanField(default=False)
  is_online = models.BooleanField(default=False)
  is_locked = models.BooleanField(default=False)
  is_superadmin_locked = models.BooleanField(default=False)

  class Meta:
    app_label = APP_LABEL

  def import_public_key(self):
    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    public_key_import = gpg.import_key(self.public_key)

    self.long_key_id = public_key_import.long_key_id
    self.save()

  def bring_online(self):
    self.is_online = True
    self.save()

  def take_offline(self):
    if self.ips.get(is_online=True) is None:
      self.is_online = False
      self.save()

  def get_connection(self, name):
    return self.connections.create(name=name, ip=self.ips.get())
