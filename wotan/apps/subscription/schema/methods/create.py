
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import BaseClientResponse
from apps.base.schema.methods.create import (
  PrototypeSchema,
)

from ..with_origin import WithOrigin, WithOriginResponse
from ..with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from .constants import create_constants

class CreateClientCreatedSchema(IndexedSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      template=TemplateSchema(types=types.UUID()),
    )

class CreateClientResponse(StructureResponse, BaseClientResponse):
  pass

class CreateClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=CreateClientResponse,
      children={
        create_constants.CREATE_COMPLETE: Schema(types=types.BOOLEAN()),
        create_constants.CREATED: CreateClientCreatedSchema(),
      },
    )

class CreateResponseWithChallenge(IndexedResponse, WithOriginResponse):
  pass

class CreateSchemaWithChallenge(WithOrigin, WithChallenge, IndexedSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      template=PrototypeSchema(Model, mode=mode),
      client=CreateClientSchema(),
    )
    self.response = CreateResponseWithChallenge

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            create_constants.CREATE_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    if self.active_response.has_errors():
      return

    temporary_ids = {}
    for prototype_temporary_id, prototype_response in self.active_response.children.items():
      created_id = prototype_response.get_id()
      temporary_ids.update({
        prototype_temporary_id: created_id,
      })

    full_queryset = self.model.objects.filter(id__in=temporary_ids.values())

    if full_queryset:
      self.active_response = self.client.respond(
        payload={
          create_constants.CREATE_COMPLETE: True,
          create_constants.CREATED: temporary_ids,
        },
      )
      self.active_response.add_internal_queryset(full_queryset)
