
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  types,
)

from .constants import with_challenge_constants
from .errors import with_challenge_errors

class WithChallengeClientSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children = merge(
      self.children,
      {
        with_challenge_constants.OPEN_CHALLENGE_ID: Schema(types=types.UUID()),
      },
    )

class WithChallenge(Schema):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.challenge_accepted = False
    self.active_challenge = None
    self.active_challenge_queryset = None

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
    if self.should_check_challenge(payload, context):
      open_challenge = context.get_account().challenges.get(origin=self.origin, is_open=True)
      if open_challenge is not None:
        self.active_response.add_error(
          with_challenge_errors.OPEN_CHALLENGE_EXISTS_WITH_ORIGIN(origin=self.origin),
        )
        return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    if self.should_check_challenge(payload, context):
      self.active_challenge = context.get_account().challenges.get(
        origin=self.origin,
        is_open=False,
        has_been_used=False,
      )

      if self.active_challenge is None:
        self.active_challenge = context.get_account().challenges.create(origin=self.origin)
        self.active_challenge.encrypt_content()
        self.active_challenge_queryset = context.get_account().challenges.filter(origin=self.origin, is_open=True)
        return

      self.active_challenge.has_been_used = True
      self.active_challenge.save()

    self.challenge_accepted = True
    super().responds_to_valid_payload(payload, context)

  def get_challenge_client_response(self):
    if self.active_challenge is not None and not self.active_challenge.has_been_used:
      return {
        with_challenge_constants.OPEN_CHALLENGE_ID: self.active_challenge._id,
      }
