
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import ResponseWithInternalQuerySet

from ....constants import address_fields
from .constants import get_constants
from .errors import get_errors

class AddressGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class AddressGetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Address get method.'
      ),
      response=AddressGetResponse,
      children={
        get_constants.ADDRESS_ID: Schema(
          description='The address ID',
          types=types.UUID(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.ADDRESS_ID_NOT_INCLUDED(),
        get_errors.ADDRESS_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if get_constants.ADDRESS_ID not in payload:
      self.active_response.add_error(
        get_errors.ADDRESS_ID_NOT_INCLUDED(),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    id = self.get_child_value(get_constants.ADDRESS_ID)
    address = self.model.objects.get(id=id)

    if not address:
      self.active_response.add_error(get_errors.ADDRESS_DOES_NOT_EXIST(id=id))
      return

    self.active_response.add_internal_queryset([address])
