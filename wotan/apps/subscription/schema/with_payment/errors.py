
from util.api import Error

class OpenPaymentExistsWithOriginError(Error):
  code = '8edc8d8edde64d12a454d78886367905'
  name = 'open_payment_exists_with_origin'
  description = 'Open payment exists with the given origin'
  description_with_arguments = 'Open payment [{}] exists with origin [{}]'

  def __init__(self, id=None, origin=None):
    self.description = (
      self.description_with_arguments.format(id, origin)
      if id is not None and origin is not None
      else self.description
    )

class PaymentsUnavailableError(Error):
  code = 'adf56cb06c7f417b86c2611399015a5e'
  name = 'payments_unavailable'
  description = 'Payments are temporarily unavailable'

class with_payment_errors:
  OPEN_PAYMENT_EXISTS_WITH_ORIGIN = OpenPaymentExistsWithOriginError
  PAYMENTS_UNAVAILABLE = PaymentsUnavailableError
