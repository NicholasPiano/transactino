
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from ......schema.with_payment import WithPayment
from .constants import activate_constants
from .errors import activate_errors

class SubscriptionActivateSchema(WithPayment, StructureSchema):
  def __init__(self):
    super().__init__(
      description=(
        'The schema for the Subscription activate method. This method is'
        ' blocked by a payment that must be closed before the method can'
        ' be completed. If you enter the ID of the subscription incorrectly,'
        ' the method will throw an error, but the payment will be valid for'
        ' each unactivated subscription until it is activated. Several payments'
        ' can be open simultaneously for different subscriptions. Refer to the'
        ' "origin" property of the subscription to check which payment'
        ' references it. Make sure you understand which subscription you are'
        ' activating by checking the relevant properties.'
      ),
      children={
        activate_constants.SUBSCRIPTION_ID: Schema(
          description='The ID of the Subscription',
          types=types.UUID(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        activate_errors.SUBSCRIPTION_ID_NOT_INCLUDED(),
        activate_errors.SUBSCRIPTION_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if activate_constants.SUBSCRIPTION_ID not in payload:
      self.active_response.add_error(
        activate_errors.SUBSCRIPTION_ID_NOT_INCLUDED(),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    subscription_id = self.get_child_value(activate_constants.SUBSCRIPTION_ID)
    subscription = context.get_account().subscriptions.get(id=subscription_id)

    if subscription is None:
      self.active_response.add_error(
        activate_errors.SUBSCRIPTION_DOES_NOT_EXIST(id=subscription_id),
      )
      return

    if not self.payment_complete(payload, context, origin=subscription.origin):
      self.prepare_payment(context, origin=subscription.origin, amount=subscription.get_btc_amount())
      return

    subscription.activate()

    self.active_response = self.client.respond(check_payment=True)
