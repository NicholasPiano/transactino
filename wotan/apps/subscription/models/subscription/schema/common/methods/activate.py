
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
from ......schema.with_payment import (
  WithPayment,
  WithPaymentClientSchema,
)
from .constants import activate_constants
from .errors import activate_errors

class SubscriptionActivateClientResponse(StructureResponse, ResponseWithExternalQuerySets):
  pass

class SubscriptionActivateClientSchema(WithPaymentClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=SubscriptionActivateClientResponse,
      children={
        activate_constants.ACTIVATION_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class SubscriptionActivateResponse(StructureResponse, WithOriginResponse):
  pass

class SubscriptionActivateSchema(WithOrigin, WithPayment, StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      client=SubscriptionActivateClientSchema(),
      children={
        activate_constants.SUBSCRIPTION_ID: Schema(types=types.UUID()),
      }
    )
    self.response = SubscriptionActivateResponse

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

  def get_subscription(self, context):
    subscription_id = self.active_response.get_child(activate_constants.SUBSCRIPTION_ID).render()
    subscription = context.get_account().subscriptions.get(id=subscription_id)

    return subscription, subscription_id

  def get_origin(self, context):
    subscription, subscription_id = self.get_subscription(context)

    if subscription is not None:
      return subscription.origin

    self.active_response.add_error(
      activate_errors.SUBSCRIPTION_DOES_NOT_EXIST(id=subscription_id),
    )

  def get_btc_amount(self, context):
    subscription, subscription_id = self.get_subscription(context)

    if subscription is not None:
      return subscription.get_cost()

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)
    if self.active_response.has_errors():
      return

    if not self.payment_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          self.get_payment_client_response(),
          {
            activate_constants.ACTIVATION_COMPLETE: False,
          },
        ),
      )
      self.active_response.add_external_queryset(self.active_payment_queryset)
      return

    subscription, subscription_id = self.get_subscription(context)
    subscription.activate()

    self.active_response = self.client.respond(
      payload={
        activate_constants.ACTIVATION_COMPLETE: True,
      },
    )
