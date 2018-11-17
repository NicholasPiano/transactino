
from django.conf import settings

from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  Response, StructureResponse,
  types, map_type,
  constants,
)

from apps.base.schema.methods.base import ResponseWithExternalQuerySets

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from ....constants import account_fields
from .constants import lock_constants

class AccountSubscribedLockClientResponse(StructureResponse, ResponseWithExternalQuerySets):
  pass

class AccountSubscribedLockClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=AccountSubscribedLockClientResponse,
      children={
        lock_constants.LOCKING_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class AccountSubscribedLockResponse(WithOriginResponse):
  pass

class AccountSubscribedLockSchema(WithOrigin, WithChallenge):
  def __init__(self, Model, **kwargs):
    super().__init__(
      **kwargs,
      types=types.BOOLEAN(),
      client=AccountSubscribedLockClientSchema(),
      origin=lock_constants.ORIGIN,
    )
    self.model = Model
    self.response = AccountSubscribedLockResponse

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            lock_constants.LOCKING_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    account = context.get_account()
    account.is_locked = self.active_response.render()
    account.save()

    self.active_response = self.client.respond(
      payload={
        lock_constants.LOCKING_COMPLETE: True,
      },
    )
