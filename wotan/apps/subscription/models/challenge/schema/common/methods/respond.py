
from django.conf import settings

from util.gpg import GPG
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse,
  types, map_type,
  constants,
)

from ....constants import challenge_fields
from .constants import respond_constants
from .errors import respond_errors

class ChallengeRespondClientSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the challenge result. Contains the'
        ' outcome of the evaluation.'
      ),
      children={
        respond_constants.CHALLENGE_ID: Schema(types=types.UUID()),
        respond_constants.IS_VERIFIED: Schema(types=types.BOOLEAN()),
      },
    )

class ChallengeRespondSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Challenge respond method.'
        ' Processes a request based on the ID of the challenge,'
        ' returning the result of the challenge evaluation.'
      ),
      client=ChallengeRespondClientSchema(),
      children={
        respond_constants.CHALLENGE_ID: Schema(
          description='The ID of the challenge in question',
          types=types.UUID(),
        ),
        respond_constants.CONTENT: Schema(
          description=(
            'The decrypted text of the challenge in ascii armor format,'
            ' having been re-encrypted to the public key of the service.'
          ),
        ),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if respond_constants.CHALLENGE_ID not in payload:
      self.active_response.add_error(respond_errors.CHALLENGE_ID_NOT_INCLUDED())

    if respond_constants.CONTENT not in payload:
      self.active_response.add_error(respond_errors.CONTENT_NOT_INCLUDED())

    if self.active_response.has_errors():
      return False

    challenge_id = payload.get(respond_constants.CHALLENGE_ID)
    challenge = context.get_account().challenges.get(id=challenge_id)

    if challenge is None:
      self.active_response.add_error(
        respond_errors.CHALLENGE_DOES_NOT_EXIST(id=challenge_id),
      )
      return False

    if challenge.has_been_used:
      self.active_response.add_error(
        respond_errors.CLOSED_CHALLENGE_HAS_BEEN_USED(id=challenge_id),
      )
      return False

    return passes_pre_response_checks

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    content_to_verify = self.active_response.get_child(respond_constants.CONTENT).render()
    challenge_id = self.active_response.get_child(respond_constants.CHALLENGE_ID).render()
    challenge = context.get_account().challenges.get(id=challenge_id)

    is_verified = challenge.verify_content(content_to_verify)

    self.active_response = self.client.respond({
      respond_constants.CHALLENGE_ID: challenge._id,
      respond_constants.IS_VERIFIED: is_verified,
    })
