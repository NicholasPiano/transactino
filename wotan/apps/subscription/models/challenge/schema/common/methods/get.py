
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
from .constants import get_constants
from .errors import get_errors

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
        get_constants.CHALLENGE_ID: Schema(
          description=(
            'The challenge ID'
          ),
          types=types.UUID(),
        ),
        challenge_fields.IS_OPEN: Schema(
          description=(
            'Filter the list of challenges'
            ' by their open states.'
          ),
          types=types.BOOLEAN(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.CHALLENGE_DOES_NOT_EXIST(),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    challenge_id = self.get_child_value(get_constants.CHALLENGE_ID)

    if challenge_id is not None:
      queryset = context.get_account().challenges.filter(id=challenge_id)

      if not queryset:
        self.active_response.add_error(
          get_errors.CHALLENGE_DOES_NOT_EXIST(id=challenge_id)
        )
        return

      self.active_response.add_internal_queryset(queryset)
      return

    queryset = context.get_account().challenges.all()

    is_open = self.get_child_value(challenge_fields.IS_OPEN)

    if is_open is not None:
      queryset = queryset.filter(is_open=is_open)

    self.active_response.add_internal_queryset(queryset)
