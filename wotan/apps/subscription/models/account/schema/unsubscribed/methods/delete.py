
from django.conf import settings

from util.merge import merge
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
from .constants import delete_constants
from .errors import delete_errors

class AccountDeleteClientResponse(StructureResponse, ResponseWithExternalQuerySets):
  pass

class AccountDeleteClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The deletion response.'
      ),
      response=AccountDeleteClientResponse,
      children={
        delete_constants.DELETION_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class AccountDeleteSchema(WithOrigin, WithChallenge):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Account delete method.'
        ' This method takes no arguments, but does'
        ' require a challenge to be solved.'
      ),
      types=types.STRUCTURE(),
      client=AccountDeleteClientSchema(),
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
    if payload:
      self.active_response.add_error(
        delete_errors.ACCOUNT_DELETE_TAKES_NO_ARGUMENTS(),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            delete_constants.DELETION_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    context.get_account().delete()

    self.active_response = self.client.respond(
      payload={
        delete_constants.DELETION_COMPLETE: True,
      },
    )
