
from util.merge import merge
from util.api import (
  Schema,
  types,
)

from ......schema.with_origin import WithOrigin
from ......schema.with_challenge import WithChallenge
from .constants import delete_constants
from .errors import delete_errors

class AccountDeleteSchema(WithOrigin, WithChallenge):
  def __init__(self):
    super().__init__(
      description=(
        'The schema for the Account delete method.'
        ' This method takes no arguments, but does'
        ' require a challenge to be solved.'
      ),
      types=types.STRUCTURE(),
      origin=delete_constants.ORIGIN,
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        delete_errors.ACCOUNT_DELETE_TAKES_NO_ARGUMENTS(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if payload:
      self.active_response.add_error(
        delete_errors.ACCOUNT_DELETE_TAKES_NO_ARGUMENTS(),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    context.get_account().delete()

    self.active_response = self.client.respond(check_challenge=True)
