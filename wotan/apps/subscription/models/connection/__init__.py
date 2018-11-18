
from django.db import models
from django.utils import timezone
from django.apps import apps

from apps.base.models import Model, Manager, model_fields

from ...constants import mode_constants, APP_LABEL
from .constants import close_codes, connection_constants, connection_fields

def get_ip(ip_value):
  IP = apps.get_model(APP_LABEL, 'IP')
  return IP.objects.get(value=ip_value, account__isnull=False)

class ConnectionManager(Manager):
  def bring_online(self, name=None, ip_value=None, port=None):
    connection, connection_created = self.get_or_create(name=name)
    if connection_created:
      connection.bring_online(
        ip=get_ip(ip_value),
        ip_value=ip_value,
        port=port,
      )

    return connection, connection_created

  def single(self, ip_value):
    return self.create(
      ip=get_ip(ip_value),
      ip_value=ip_value,
    )

class Connection(Model):
  objects = ConnectionManager()

  ip = models.ForeignKey(
    connection_constants.IP_RELATED_MODEL,
    related_name=connection_constants.IP_RELATED_NAME,
    on_delete=models.CASCADE,
    null=True,
  )

  ip_value = models.CharField(max_length=255, null=True)
  is_online = models.BooleanField(default=False)
  port = models.PositiveIntegerField(null=True)
  name = models.CharField(max_length=255, null=True)
  closed_at = models.DateTimeField(null=True)
  closed_with_code = models.PositiveIntegerField(null=True)

  class Meta:
    app_label = APP_LABEL

  def bring_online(self, ip=None, ip_value=None, port=None):
    self.is_online = True
    self.ip = ip
    self.ip_value = ip_value
    self.port = port
    self.save()

    if self.ip is not None:
      self.ip.bring_online()

  def take_offline(self, code=None):
    self.is_online = False
    self.closed_at = timezone.now()
    self.closed_with_code = code
    self.save()

    if self.ip is not None:
      self.ip.take_offline()
