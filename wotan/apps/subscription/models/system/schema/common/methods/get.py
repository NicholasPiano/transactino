
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import ResponseWithInternalQuerySet

from ....constants import system_fields
from .errors import get_errors

class SystemGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class SystemGetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the System get method.'
        ' Returns details about the system'
        ' including the public key and long key id.'
      ),
      response=SystemGetResponse,
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.SYSTEM_GET_TAKES_NO_ARGUMENTS(),
        get_errors.NO_SYSTEM(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if payload:
      self.active_response.add_error(
        get_errors.SYSTEM_GET_TAKES_NO_ARGUMENTS(),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    system = self.model.objects.active()

    if not system:
      self.active_response.add_error(get_errors.NO_SYSTEM())
      return

    self.active_response.add_internal_queryset([system])
