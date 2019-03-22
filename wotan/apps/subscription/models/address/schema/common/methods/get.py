
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
        ' Returns the active address for use in'
        ' payments.'
      ),
      response=AddressGetResponse,
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.ADDRESS_GET_TAKES_NO_ARGUMENTS(),
        get_errors.NO_ADDRESS(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if payload:
      self.active_response.add_error(
        get_errors.ADDRESS_GET_TAKES_NO_ARGUMENTS(),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    address = self.model.objects.get_active_address()

    if not address:
      self.active_response.add_error(get_errors.NO_ADDRESS())
      return

    self.active_response.add_internal_queryset([address])
