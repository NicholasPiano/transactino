
from util.api import (
  Schema,
  types,
)

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import WithChallenge
from .constants import get_constants
from .errors import get_errors

class IPGetResponse(WithOriginResponse):
  pass

class IPGetSchema(WithOrigin, WithChallenge):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the IP get method. This method returns'
        ' ALL IP addresses bound to this account.'
      ),
      types=types.STRUCTURE(),
      origin=get_constants.ORIGIN,
      response=IPGetResponse,
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.IP_GET_TAKES_NO_ARGUMENTS(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if payload:
      self.active_response.add_error(
        get_errors.IP_GET_TAKES_NO_ARGUMENTS(),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    self.active_response = self.client.respond(check_challenge=True)
    self.active_response.add_internal_queryset(context.get_account().ips.all())
