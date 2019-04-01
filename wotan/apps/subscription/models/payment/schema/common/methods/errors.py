
from util.api import Error

class PaymentDoesNotExistError(Error):
  code = '10091'
  name = 'payment_does_not_exist'
  description = 'Payment does not exist'
  description_with_arguments = 'Payment with id [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class get_errors:
  PAYMENT_DOES_NOT_EXIST = PaymentDoesNotExistError
