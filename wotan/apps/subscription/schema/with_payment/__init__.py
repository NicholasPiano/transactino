
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from apps.base.schema.methods.base import BaseClientResponse

from ...models.address import Address
from ...models.discount import Discount
from .constants import with_payment_constants
from .errors import with_payment_errors

class WithPaymentClientResponse(StructureResponse, BaseClientResponse):
  pass

class WithPaymentClientSchema(StructureSchema):
  def __init__(self, response=WithPaymentClientResponse, children={}, **kwargs):
    super().__init__(
      **kwargs,
      response=response,
      children=merge(
        {
          with_payment_constants.PAYMENT_COMPLETE: Schema(types=types.BOOLEAN()),
          with_payment_constants.OPEN_PAYMENT_ID: Schema(types=types.UUID()),
        },
        children,
      ),
    )

  def respond(self, payload={}, context=None, payment_id=None, check_payment=False, **kwargs):
    if not check_payment:
      return super().respond(payload=payload, context=context, **kwargs)

    payload = merge(
      payload,
      {
        with_payment_constants.PAYMENT_COMPLETE: payment_id is None,
      },
    )

    if payment_id is not None:
      payload = merge(
        payload,
        {
          with_payment_constants.OPEN_PAYMENT_ID: payment_id,
        },
      )

    return super().respond(payload=payload, context=context, **kwargs)

class WithPayment(Schema):
  def __init__(self, client=WithPaymentClientSchema(), **kwargs):
    super().__init__(
      **kwargs,
      client=client,
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        with_payment_errors.OPEN_PAYMENT_EXISTS_WITH_ORIGIN(),
        with_payment_errors.PAYMENTS_UNAVAILABLE(),
      },
    )

  def should_check_payment(self, payload, context):
    return True

  def get_btc_amount(self):
    raise NotImplementedError('Define a cost for making a payment')

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if not self.should_check_payment(payload, context):
      return True

    open_payment = context.get_account().payments.get(origin=self.origin, is_open=True)
    if open_payment is not None:
      self.active_response.add_error(
        with_payment_errors.OPEN_PAYMENT_EXISTS_WITH_ORIGIN(id=open_payment._id, origin=self.origin),
      )
      return False

    closed_payment = context.get_account().payments.get(
      origin=self.origin,
      is_open=False,
      has_been_used=False,
    )

    if closed_payment is None:
      address = Address.objects.get_active_address()

      if not address:
        self.active_response.add_error(
          with_payment_errors.PAYMENTS_UNAVAILABLE(),
        )
        return

      new_payment = context.get_account().payments.create(
        origin=self.origin,
        address=address,
        base_amount=self.get_btc_amount(context),
      )
      new_payment.prepare()
      self.active_response = self.client.respond(payment_id=new_payment._id, check_payment=True)
      self.active_response.add_external_queryset([new_payment])
      return False

    closed_payment.has_been_used = True
    closed_payment.save()

    return True
