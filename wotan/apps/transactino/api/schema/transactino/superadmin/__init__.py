
from util.api import Schema

from .constants import superadmin_constants
from .status import StatusSchema, should_enter_status_schema, strip_access
from .schema import SuperadminTopLevelSchema

class SuperadminSchema(Schema):
  def respond(self, payload=None, context=None):
    # if payload is not None and superadmin_constants.STATUS in payload:
    #   return StatusSchema().respond(payload=payload, context=context)
    #
    # payload_without_access = strip_access(payload)

    return SuperadminTopLevelSchema().respond(payload=payload, context=context)

def should_enter_superadmin_schema(payload, context):
  return context.is_superadmin()
  # if payload is not None and superadmin_constants.STATUS in payload:
  #   return True
