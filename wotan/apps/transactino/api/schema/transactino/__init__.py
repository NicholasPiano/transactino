
from util.api import Schema

from ..context import TransactinoContext
from .errors import transactino_errors
from .anonymous import AnonymousSchema
from .subscribed import SubscribedSchema
from .unsubscribed import UnsubscribedSchema
from .superadmin import SuperadminSchema, should_enter_superadmin_schema

class TransactinoSchema(Schema):
  def respond(self, system=None, connection=None, payload=None):
    if system is None:
      response = self.get_response()
      response.add_error(
        transactino_errors.NO_ACTIVE_SYSTEM(),
      )
      return response

    context = TransactinoContext(system=system, connection=connection)

    if should_enter_superadmin_schema(payload, context):
      return SuperadminSchema().respond(payload=payload, context=context)

    if context.is_anonymous():
      return AnonymousSchema().respond(payload=payload, context=context)

    if context.is_subscribed():
      return SubscribedSchema().respond(payload=payload, context=context)

    return UnsubscribedSchema(context=context).respond(payload=payload, context=context)
