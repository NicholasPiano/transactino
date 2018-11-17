
from util.merge import merge
from util.api import (
  Schema, StructureSchema, IndexedSchema,
  Response, StructureResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import BaseClientResponse
from apps.base.schema.methods.set import (
  SetResponse,
  PrototypeSchema,
)

from ..with_origin import WithOrigin, WithOriginResponse
from ..with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from .constants import set_constants

class SetClientResponseWithChallenge(StructureResponse, BaseClientResponse):
  pass

class SetClientSchemaWithChallenge(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=SetClientResponseWithChallenge,
      children={
        set_constants.SET_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class SetResponseWithChallenge(SetResponse, WithOriginResponse):
  pass

class SetSchemaWithChallenge(WithOrigin, WithChallenge, IndexedSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      template=PrototypeSchema(Model, mode=mode),
      client=SetClientSchemaWithChallenge(),
    )
    self.response = SetResponseWithChallenge

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            set_constants.SET_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    if self.active_response.has_errors():
      return

    full_queryset = self.model.objects.filter(id__in=self.active_response.children.keys())

    if full_queryset:
      self.active_response = self.client.respond(
        payload={
          set_constants.SET_COMPLETE: True,
        },
      )
      self.active_response.add_internal_queryset(full_queryset)
