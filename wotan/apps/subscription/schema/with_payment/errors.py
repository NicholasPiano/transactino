
from util.api import Error

class OpenPaymentExistsWithOriginError(Error):
  code = '725'
  name = 'open_payment_exists_with_origin'
  description = 'Open payment exists with the given origin'
  description_with_arguments = 'Open payment exists with origin [{}]'

  def __init__(self, origin=None):
    self.description = (
      self.description_with_arguments.format(origin)
      if origin is not None
      else self.description
    )

class PaymentsUnavailableError(Error):
  code = '727'
  name = 'payments_unavailable'
  description = 'Payments are temporarily unavailable'

class with_payment_errors:
  OPEN_PAYMENT_EXISTS_WITH_ORIGIN = OpenPaymentExistsWithOriginError
  PAYMENTS_UNAVAILABLE = PaymentsUnavailableError
