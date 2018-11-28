
import json

from util.api import Schema, StructureSchema, types

from apps.subscription.models import Connection

from .constants import proxy_constants
from .transactino import TransactinoSchema

class ProxySchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      proxy_constants.ID: Schema(types=types.UUID()),
      proxy_constants.IP: Schema(),
      proxy_constants.CHANNEL: Schema(),
      proxy_constants.TRANSACTINO: Schema(types=types.ANY()),
    }

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)
    if self.active_response.has_errors():
      return

    connection, connection_created = Connection.objects.bring_online(
      name=self.active_response.get_child(proxy_constants.CHANNEL).render(),
      ip_value=self.active_response.get_child(proxy_constants.IP).render(),
    )

    self.active_response.add_child(
      proxy_constants.TRANSACTINO,
      TransactinoSchema().respond(
        connection=connection,
        payload=payload.get(proxy_constants.TRANSACTINO),
      )
    )
