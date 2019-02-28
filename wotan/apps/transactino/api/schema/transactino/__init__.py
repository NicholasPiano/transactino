
from util.api import Schema

from ..context import TransactinoContext
from .anonymous import AnonymousSchema
from .subscribed import SubscribedSchema
from .unsubscribed import UnsubscribedSchema
from .superadmin import SuperadminSchema, should_enter_superadmin_schema

class TransactinoSchema(Schema):
  def respond(self, connection=None, payload=None):
    context = TransactinoContext(connection=connection)

    if should_enter_superadmin_schema(payload, context):
      return SuperadminSchema().respond(payload=payload, context=context)

    if context.is_anonymous():
      return AnonymousSchema().respond(payload=payload, context=context)

    if context.is_subscribed():
      return SubscribedSchema().respond(payload=payload, context=context)

    return UnsubscribedSchema(context=context).respond(payload=payload, context=context)
