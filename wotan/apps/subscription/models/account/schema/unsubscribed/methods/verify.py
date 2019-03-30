
from django.conf import settings

from util.merge import merge
from util.api import (
  Schema,
  types,
)

from ......schema.with_origin import WithOrigin
from ......schema.with_challenge import WithChallenge, WithChallengeClientSchema
from ....constants import account_fields
from .constants import verify_constants
from .errors import verify_errors

class Client(WithChallengeClientSchema):
  def respond(self, payload=None, context=None):
    print('CLIENT PAYLOAD', payload)
    return super().respond(payload=payload, context=context)

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
      origin=verify_constants.ORIGIN,
      client=Client(),
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
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if payload:
      self.active_response.add_error(
        verify_errors.ACCOUNT_VERIFY_TAKES_NO_ARGUMENTS(),
      )
      return False

    if context.get_account().is_verified:
      self.active_response.add_error(
        verify_errors.ACCOUNT_ALREADY_VERIFIED(),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    account = context.get_account()
    account.is_verified = True
    account.save()

    self.active_response = self.client.respond()
