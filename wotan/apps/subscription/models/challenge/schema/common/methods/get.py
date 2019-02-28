
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import ResponseWithInternalQuerySet

from ....constants import challenge_fields

class ChallengeGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class ChallengeGetSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Challenge get method.'
        ' Returns instances of the Challenge class and'
        ' includes a simple filter for the open status'
        ' of each object.'
      ),
      response=ChallengeGetResponse,
      children={
        challenge_fields.IS_OPEN: Schema(
          description=(
            'A value intended to filter the list of challenges'
            ' by its open state.'
          ),
          types=types.BOOLEAN(),
        ),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    is_open = self.active_response.force_get_child(challenge_fields.IS_OPEN).render()

    queryset = []
    if is_open is None:
      queryset = context.get_account().challenges.all()
    else:
      queryset = context.get_account().challenges.filter(is_open=is_open)

    self.active_response.add_internal_queryset(queryset)
