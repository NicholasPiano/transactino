
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import BaseClientResponse

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from .constants import get_constants
from .errors import get_errors

class IPGetClientResponse(StructureResponse, BaseClientResponse):
  pass

class IPGetClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=IPGetClientResponse,
      children={
        get_constants.GET_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class IPGetResponse(WithOriginResponse):
  pass

class IPGetSchema(WithOrigin, WithChallenge):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the IP get method.'
      ),
      types=types.STRUCTURE(),
      client=IPGetClientSchema(),
      origin=get_constants.ORIGIN,
    )
    self.response = IPGetResponse

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.IP_GET_TAKES_NO_ARGUMENTS(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if payload:
      self.active_response.add_error(
        get_errors.IP_GET_TAKES_NO_ARGUMENTS(),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            get_constants.GET_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    self.active_response = self.client.respond(
      payload={
        get_constants.GET_COMPLETE: True,
      },
    )
    self.active_response.add_internal_queryset(context.get_account().ips.all())
