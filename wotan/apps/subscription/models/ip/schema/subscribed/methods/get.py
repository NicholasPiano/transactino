
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import WithChallenge
from .constants import get_constants
from .errors import get_errors

class IPGetResponse(StructureResponse, WithOriginResponse):
  pass

class IPGetSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the IP get method. IP addresses can be fetched by'
        ' their ID. The default behaviour if no ID is included is to return'
        ' all IP addresses bound to this account.'
      ),
      origin=get_constants.ORIGIN,
      response=IPGetResponse,
      children={
        get_constants.IP_ID: Schema(
          description=(
            'The IP address ID'
          ),
          types=types.UUID(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.IP_DOES_NOT_EXIST(),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    queryset = context.get_account().ips.all()

    ip_id = self.get_child_value(get_constants.IP_ID)
    if ip_id is not None:
      queryset = queryset.filter(id=ip_id)

    if not queryset:
      self.active_response.add_error(
        get_errors.IP_DOES_NOT_EXIST(id=ip_id)
      )
      return

    self.active_response = self.client.respond(check_challenge=True)
    self.active_response.add_internal_queryset(queryset)
