
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
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

class IPDeleteClientResponse(StructureResponse, ResponseWithExternalQuerySets):
  pass

class IPDeleteClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=IPDeleteClientResponse,
      children={
        delete_constants.DELETE_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class IPDeleteResponse(WithOriginResponse):
  pass

class IPDeleteSchema(WithOrigin, WithChallenge):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the IP delete method.'
      ),
      client=IPDeleteClientSchema(),
      origin=delete_constants.ORIGIN,
    )
    self.response = IPDeleteResponse

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        delete_errors.IP_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if not context.get_account().ips.filter(value=payload).count():
      self.active_response.add_error(
        delete_errors.IP_DOES_NOT_EXIST(value=payload),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            delete_constants.DELETE_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    ip = context.get_account().ips.get(value=payload)
    ip.delete()

    self.active_response = self.client.respond(
      payload={
        delete_constants.DELETE_COMPLETE: True,
      },
    )
