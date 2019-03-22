
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  types,
)

from ...models.address import Address
from ...models.discount import Discount
from .constants import with_payment_constants
from .errors import with_payment_errors

class WithPaymentClientSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children = merge(
      self.children,
      {
        with_payment_constants.OPEN_PAYMENT_ID: Schema(types=types.UUID()),
      },
    )

class WithPayment(Schema):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.payment_accepted = False
    self.active_payment = None
    self.active_payment_queryset = None

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        with_payment_errors.OPEN_PAYMENT_EXISTS_WITH_ORIGIN(),
      },
    )

  def should_check_payment(self, payload, context):
    return True

  def get_origin(self, context):
    return self.origin

  def get_btc_amount(self):
    raise NotImplementedError('Define a cost for making a payment')

  def get_payment_client_response(self):
    if self.active_payment is not None and not self.active_payment.has_been_used:
      return {
        with_payment_constants.OPEN_PAYMENT_ID: self.active_payment._id,
      }

  def get_discount(self):
    if self.active_response.has_child(with_payment_constants.DISCOUNT):
      discount_id = self.active_response.get_child(with_payment_constants.DISCOUNT)
      discount = Discount.objects.consume(id=discount_id)
      if discount is not None:
        return discount.value

  def passes_pre_response_checks(self, payload, context):
    if with_payment_constants.DISCOUNT in payload:
      payload_without_discount = {
        key: p.get(key)
        for key in payload
        if key != with_payment_constants.DISCOUNT
      }
      return super().passes_pre_response_checks(payload_without_discount, context)

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    if self.should_check_payment(payload, context):
      origin = self.get_origin(context)

      open_payment = context.get_account().payments.get(origin=origin, is_open=True)
      if open_payment is not None:
        self.active_response.add_error(
          with_payment_errors.OPEN_PAYMENT_EXISTS_WITH_ORIGIN(origin=origin),
        )
        return

      self.active_payment = context.get_account().payments.get(
        origin=origin,
        is_open=False,
        has_been_used=False,
      )

      if self.active_payment is None:
        to_address = Address.objects.get_active_address()

        if not to_address:
          self.active_response.add_error(
            with_payment_errors.PAYMENTS_UNAVAILABLE(),
          )
          return

        base_amount = self.get_discount() or self.get_btc_amount(context)
        self.active_payment = context.get_account().payments.create(
          to_address=to_address,
          origin=origin,
          base_amount=base_amount,
        )

        self.active_payment.prepare()
        self.active_payment_queryset = context.get_account().payments.filter(origin=origin, is_open=True)
        return

      self.active_payment.has_been_used = True
      self.active_payment.save()

    self.payment_accepted = True
