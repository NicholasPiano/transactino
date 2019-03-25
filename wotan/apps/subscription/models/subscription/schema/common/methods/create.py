
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
      },
    )

class SubscriptionCreateResponse(StructureResponse, WithOriginResponse):
  pass

class SubscriptionCreateSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Subscription create method.'
        ' This method can be run without arguments to create a challenge'
        ' originating from the method. When run with arguments, a duration'
        ' is required.'
      ),
      origin=create_constants.ORIGIN,
      client=SubscriptionCreateClientSchema(),
      children={
        subscription_fields.DURATION_IN_DAYS: Schema(
          description=(
            'The duration, measured in periods of 24 hours'
            ' from the date of activation.'
          ),
          types=types.INTEGER(),
        ),
        subscription_fields.ACTIVATION_DATE: Schema(
          description=(
            'The activation date. This can be given as any valid date string.'
            ' Once this date is passed, a process will run that verifies and activates'
            ' the subscription. From this point, a request made from any IP address'
            ' associated with the account will be responded to accordingly.'
          ),
          types=types.TIME(),
        ),
      },
    )
    self.response = SubscriptionCreateResponse

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        create_errors.DURATION_NOT_INCLUDED(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if self.closed_unused_challenge_exists() and subscription_fields.DURATION_IN_DAYS not in payload:
      self.active_response.add_error(
        create_errors.DURATION_NOT_INCLUDED(),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            create_constants.CREATE_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    duration_in_days = self.active_response.get_child(subscription_fields.DURATION_IN_DAYS).render()
    activation_date = self.active_response.force_get_child(subscription_fields.ACTIVATION_DATE).render()

    subscription = context.get_account().subscriptions.create(
      duration_in_days=duration_in_days,
      activation_date=activation_date,
    )

    self.active_response = self.client.respond(
      payload={
        create_constants.CREATE_COMPLETE: True,
      },
    )
    self.active_response.add_internal_queryset(
      context.get_account().subscriptions.filter(id=subscription._id),
    )
