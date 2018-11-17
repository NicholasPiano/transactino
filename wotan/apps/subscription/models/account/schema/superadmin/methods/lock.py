
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
from .errors import account_superadmin_method_errors

class AccountSuperadminLockClientResponse(StructureResponse, ResponseWithExternalQuerySets):
  pass

class AccountSuperadminLockClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=AccountSuperadminLockClientResponse,
      children={
        lock_constants.LOCKING_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class AccountSuperadminLockResponse(StructureResponse, WithOriginResponse):
  pass

class AccountSuperadminLockSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(
      **kwargs,
      client=AccountSuperadminLockClientSchema(),
      origin=lock_constants.ORIGIN,
      children={
        lock_constants.LOCK: Schema(types=types.BOOLEAN()),
        lock_constants.ACCOUNT: Schema(types=types.UUID()),
      },
    )
    self.model = Model
    self.response = AccountSuperadminLockResponse

  def passes_pre_response_checks(self, payload, context):

    if lock_constants.ACCOUNT not in payload:
      self.active_response.add_error(account_superadmin_method_errors.ACCOUNT_NOT_INCLUDED())
      return False

    return super().passes_pre_response_checks(payload, context)

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

    account_id = self.active_response.get_child(lock_constants.ACCOUNT).render()
    account = self.model.objects.get(id=account_id)

    should_lock = self.active_response.force_get_child(lock_constants.LOCK).render()

    account.is_superadmin_locked = should_lock
    account.save()

    self.active_response = self.client.respond(
      payload={
        lock_constants.LOCKING_COMPLETE: True,
      },
    )
