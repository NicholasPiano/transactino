
from util.api import Error

class TransactionReportDoesNotExistError(Error):
  code = '1028'
  name = 'transaction_report_does_not_exist'
  description = 'TransactionReport does not exist'
  description_with_arguments = 'TransactionReport with id [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class delete_errors:
  TRANSACTION_REPORT_DOES_NOT_EXIST = TransactionReportDoesNotExistError

class TransactionReportIDNotIncludedError(Error):
  code = '1029'
  name = 'transaction_report_id_not_included'
  description = 'TransactionReport ID must be included'

class activate_errors:
  TRANSACTION_REPORT_DOES_NOT_EXIST = TransactionReportDoesNotExistError
  TRANSACTION_REPORT_ID_NOT_INCLUDED = TransactionReportIDNotIncludedError
