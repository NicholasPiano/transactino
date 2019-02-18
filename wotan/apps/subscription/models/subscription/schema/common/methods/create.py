
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  Response, StructureResponse,
  types, map_type,
  constants,
)

from apps.base.schema.methods.base import BaseClientResponse

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from ....constants import subscription_fields
from .constants import create_constants
from .errors import create_errors

class SubscriptionCreateClientResponse(StructureResponse, BaseClientResponse):
  pass

class SubscriptionCreateClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=SubscriptionCreateClientResponse,
      children={
        create_constants.CREATE_COMPLETE: Schema(types=types.BOOLEAN()),
        # create_constants.ID_FOR_COMPLETION: Schema(types=types.UUID()),
      },
    )

class SubscriptionCreateResponse(StructureResponse, WithOriginResponse):
  pass

class SubscriptionCreateSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      origin=create_constants.ORIGIN,
      client=SubscriptionCreateClientSchema(),
      children={
        subscription_fields.DURATION_IN_DAYS: Schema(types=types.INTEGER()),
        subscription_fields.ACTIVATION_DATE: Schema(types=types.TIME()),
      },
    )
    self.response = SubscriptionCreateResponse

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        create_errors.DURATION_NOT_INCLUDED(),
        # invalid subscription id
        # too many arguments
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if not super().passes_pre_response_checks(payload, context):
      return False

    if subscription_fields.DURATION_IN_DAYS not in payload:
      self.active_response.add_error(
        create_errors.DURATION_NOT_INCLUDED(),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    duration_in_days = self.active_response.get_child(subscription_fields.DURATION_IN_DAYS).render()
    activation_date = self.active_response.force_get_child(subscription_fields.ACTIVATION_DATE).render()

    subscription = context.get_account().subscriptions.create(
      duration_in_days=duration_in_days,
      activation_date=activation_date,
    )

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            create_constants.CREATE_COMPLETE: False,
            # create_constants.ID_FOR_COMPLETION: subscription._id,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    # subscription.complete_creation()
    self.active_response = self.client.respond(
      payload={
        create_constants.CREATE_COMPLETE: True,
      },
    )
    self.active_response.add_internal_queryset(
      context.get_account().subscriptions.filter(id=subscription._id),
    )
