
from django.conf import settings

from util.merge import merge
from util.gpg import GPG
from util.api import (
  Schema, StructureSchema,
  Response, StructureResponse,
  types, map_type,
  constants,
)

from apps.base.schema.methods.base import ResponseWithExternalQuerySets

from ......schema.with_origin import WithOrigin
from ......schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from ....constants import account_fields
from .constants import verify_constants
from .errors import verify_errors

class AccountVerifyClientResponse(StructureResponse, ResponseWithExternalQuerySets):
  pass

class AccountVerifyClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The verification response'
      ),
      response=AccountVerifyClientResponse,
      children={
        verify_constants.VERIFICATION_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class AccountVerifySchema(WithOrigin, WithChallenge):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Account verify method.'
        ' This method takes no arguments, but does require'
        ' a challenge to be solved.'
      ),
      types=types.STRUCTURE(),
      client=AccountVerifyClientSchema(),
      origin=verify_constants.ORIGIN,
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        verify_errors.ACCOUNT_VERIFY_TAKES_NO_ARGUMENTS(),
        verify_errors.ACCOUNT_ALREADY_VERIFIED(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if payload:
      self.active_response.add_error(
        verify_errors.ACCOUNT_VERIFY_TAKES_NO_ARGUMENTS(),
      )
      return False

    if context.get_account().is_verified:
      self.active_response.add_error(
        verify_errors.ACCOUNT_ALREADY_VERIFIED(),
      )

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            verify_constants.VERIFICATION_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    account = context.get_account()
    account.is_verified = True
    account.save()

    self.active_response = self.client.respond(
      payload={
        verify_constants.VERIFICATION_COMPLETE: True,
      },
    )
