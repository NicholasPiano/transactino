
from ..with_payment import WithPayment

class WithFixedPayment(WithPayment):
  def get_btc_amount(self):
    raise NotImplementedError('Define a cost for making a payment')

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if not self.payment_complete(payload, context, origin=self.origin):
      self.prepare_payment(context, origin=self.origin, amount=self.get_btc_amount())
      return False

    return True
