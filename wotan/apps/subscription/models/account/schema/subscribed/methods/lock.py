
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

class AccountSubscribedLockResponse(StructureResponse, WithOriginResponse):
  pass

class AccountSubscribedLockSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model):
    self.model = Model
    super().__init__(
      description=(
        'Schema for the Account lock method.'
        ' Once lock is set to true, the account will be unusable'
        ' until lock is set to false by calling this method again.'
      ),
      response=AccountSubscribedLockResponse,
      origin=lock_constants.ORIGIN,
      children={
        lock_constants.LOCK: Schema(
          description=(
            'Value specifying the desired lock state of the account'
          ),
          types=types.BOOLEAN(),
        ),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    account = context.get_account()

    lock = self.get_child_value(lock_constants.LOCK)

    account.is_locked = lock if lock is not None else True
    account.save()

    self.active_response = self.client.respond(check_challenge=True)
