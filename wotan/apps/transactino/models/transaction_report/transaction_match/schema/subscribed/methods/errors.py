
from util.api import Error

class TransactionMatchDoesNotExistError(Error):
  code = '10281'
  name = 'transaction_match_does_not_exist'
  description = 'TransactionMatch does not exist'
  description_with_arguments = 'TransactionMatch with id [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class get_errors:
  TRANSACTION_MATCH_DOES_NOT_EXIST = TransactionMatchDoesNotExistError
