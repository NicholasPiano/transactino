
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  types,
)

from .constants import delete_constants
from .errors import delete_errors

class ChallengeDeleteSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Challenge delete method.'
      ),
      children={
        delete_constants.CHALLENGE_ID: Schema(
          description=(
            'The challenge ID to delete'
          ),
          types=types.UUID(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        delete_errors.CHALLENGE_ID_NOT_INCLUDED(),
        delete_errors.CHALLENGE_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if delete_constants.CHALLENGE_ID not in payload:
      self.active_response.add_error(delete_errors.CHALLENGE_ID_NOT_INCLUDED())
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    challenge_id = self.get_child_value(delete_constants.CHALLENGE_ID)
    challenge = context.get_account().challenges.get(id=challenge_id)

    if challenge is None:
      self.active_response.add_error(
        delete_errors.CHALLENGE_DOES_NOT_EXIST(id=challenge_id)
      )
      return

    challenge.delete()
