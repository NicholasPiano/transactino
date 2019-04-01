
from django.conf import settings

from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import WithChallenge
from ....constants import account_fields
from .constants import lock_constants
from .errors import lock_errors

class AccountSuperadminLockResponse(StructureResponse, WithOriginResponse):
  pass

class AccountSuperadminLockSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model):
    self.model = Model
    super().__init__(
      origin=lock_constants.ORIGIN,
      response=AccountSuperadminLockResponse,
      children={
        lock_constants.LOCK: Schema(types=types.BOOLEAN()),
        lock_constants.ACCOUNT_ID: Schema(types=types.UUID()),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        lock_errors.ACCOUNT_ID_NOT_INCLUDED(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if lock_constants.ACCOUNT_ID not in payload:
      self.active_response.add_error(lock_errors.ACCOUNT_ID_NOT_INCLUDED())
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    account_id = self.get_child_value(lock_constants.ACCOUNT_ID)
    account = self.model.objects.get(id=account_id)

    lock = self.get_child_value(lock_constants.LOCK)

    account.is_superadmin_locked = lock if lock is not None else True
    account.save()

    self.active_response = self.client.respond(check_challenge=True)
