
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
from ..with_challenge import WithChallenge
from .constants import set_constants

class SetResponseWithChallenge(SetResponse, WithOriginResponse):
  pass

class SetSchemaWithChallenge(WithOrigin, WithChallenge, IndexedSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=SetResponseWithChallenge,
      template=PrototypeSchema(Model, mode=mode),
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    full_queryset = self.model.objects.filter(id__in=self.active_response.children.keys())

    self.active_response = self.client.respond()
    self.active_response.add_internal_queryset(full_queryset)
