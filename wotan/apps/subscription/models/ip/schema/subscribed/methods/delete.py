
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  Response, StructureResponse,
  types,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import ResponseWithExternalQuerySets

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from .constants import delete_constants
from .errors import delete_errors

class IPDeleteResponse(StructureResponse, WithOriginResponse):
  pass

class IPDeleteSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the IP delete method.'
      ),
      origin=delete_constants.ORIGIN,
      response=IPDeleteResponse,
      children={
        delete_constants.IP_ID: Schema(types=types.UUID()),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        delete_errors.IP_ID_NOT_INCLUDED(),
        delete_errors.IP_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if delete_constants.IP_ID not in payload:
      self.active_response.add_error(
        delete_errors.IP_ID_NOT_INCLUDED(),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    ip_id = self.get_child_value(delete_constants.IP_ID)
    ip = context.get_account().ips.get(id=ip_id)

    if ip is None:
      self.active_response.add_error(
        delete_errors.IP_DOES_NOT_EXIST(id=ip_id),
      )
      return

    ip.delete()

    self.active_response = self.client.respond(check_challenge=True)
