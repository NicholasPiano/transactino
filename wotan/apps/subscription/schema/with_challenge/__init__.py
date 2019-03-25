
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from apps.base.schema.methods.base import BaseClientResponse

from .constants import with_challenge_constants
from .errors import with_challenge_errors

class WithChallengeClientResponse(StructureResponse, BaseClientResponse):
  pass

class WithChallengeClientSchema(StructureSchema):
  def __init__(self, children={}, **kwargs):
    super().__init__(
      **kwargs,
      response=WithChallengeClientResponse,
      children=merge(
        {
          with_challenge_constants.CHALLENGE_COMPLETE: Schema(types=types.BOOLEAN()),
          with_challenge_constants.OPEN_CHALLENGE_ID: Schema(types=types.UUID()),
        },
        children,
      ),
    )

  def respond(self, payload=None, context=None, challenge_id=None):
    payload = merge(
      payload,
      {
        with_challenge_constants.CHALLENGE_COMPLETE: challenge_id is None,
      },
    )

    if challenge_id is not None:
      payload = merge(
        payload,
        {
          with_challenge_constants.OPEN_CHALLENGE_ID: challenge_id,
        },
      )

    return super().respond(payload=payload, context=context)

class WithChallenge(Schema):
  def __init__(self, client=None, **kwargs):
    super().__init__(
      **kwargs,
      client=(
        client or WithChallengeClientSchema()
      ),
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        with_challenge_errors.OPEN_CHALLENGE_EXISTS_WITH_ORIGIN(),
      },
    )

  def should_check_challenge(self, payload, context):
    return True

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if not self.should_check_challenge(payload, context):
      return passes_pre_response_checks

    open_challenge = context.get_account().challenges.get(origin=self.origin, is_open=True)
    if open_challenge is not None:
      self.active_response.add_error(
        with_challenge_errors.OPEN_CHALLENGE_EXISTS_WITH_ORIGIN(id=open_challenge._id, origin=self.origin),
      )
      return False

    closed_challenge = context.get_account().challenges.get(
      origin=self.origin,
      is_open=False,
      has_been_used=False,
    )

    if closed_challenge is None:
      new_challenge = context.get_account().challenges.create(origin=self.origin)
      new_challenge.encrypt_content()
      self.active_response = self.client.respond(challenge_id=new_challenge._id)
      self.active_response.add_external_queryset([new_challenge])
      return False

    closed_challenge.has_been_used = True
    closed_challenge.save()

    return True
