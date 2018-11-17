
import json

from django.views import View
from django.http import JsonResponse
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from apps.subscription.models import Connection

from .methods import ConsumerMethodsMixin
from .constants import api_constants, consumer_constants
from .schema import TransactinoSchema

def api(connection=None, payload=None):
  return TransactinoSchema().respond(connection=connection, payload=payload).render()

class TransactinoConsumer(JsonWebsocketConsumer, ConsumerMethodsMixin):
  def send_payload(self, payload=None):
    self.send_json(api(connection=self.connection, payload=payload))

  def connect(self):
    [ip_value, port] = self.scope.get(consumer_constants.CLIENT)
    self.connection, connection_created = Connection.objects.bring_online(
      name=self.channel_name,
      ip_value=ip_value,
      port=port,
    )

    if connection_created:
      self.accept()
      self.send_payload()

  def receive_json(self, payload):
    self.send_payload(payload=payload)

  def disconnect(self, close_code):
    self.connection.take_offline(code=close_code)

def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    return x_forwarded_for.split(',')[0]

  return request.META.get('REMOTE_ADDR')

class TransactinoView(View):
  def get(self, request):
    connection = Connection.objects.single(ip_value=get_client_ip(request))
    return JsonResponse(api(connection=connection))

  def post(self, request):
    connection = Connection.objects.single(ip_value=get_client_ip(request))
    return JsonResponse(api(connection=connection, payload=json.loads(request.body)))
