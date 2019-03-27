
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  Response, StructureResponse,
  types,
)

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import WithChallenge
from ....constants import subscription_fields
from .constants import create_constants
from .errors import create_errors

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
      response=SubscriptionCreateResponse,
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

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        create_errors.DURATION_NOT_INCLUDED(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
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

    duration_in_days = self.get_child_value(subscription_fields.DURATION_IN_DAYS)
    activation_date = self.get_child_value(subscription_fields.ACTIVATION_DATE)

    subscription = context.get_account().subscriptions.create(
      duration_in_days=duration_in_days,
      activation_date=activation_date,
    )

    self.active_response = self.client.respond()
    self.active_response.add_internal_queryset([subscription])
