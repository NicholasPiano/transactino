
from util.api import Error

class FeeReportIDNotIncludedError(Error):
  code = '19d3845a6da8487082a29e292259f3ec'
  name = 'fee_report_id_not_included'
  description = 'FeeReport ID must be included'

class FeeReportDoesNotExistError(Error):
  code = 'a559b6b4e6884695b37bb586dcd60ca2'
  name = 'fee_report_does_not_exist'
  description = 'FeeReport does not exist'
  description_with_arguments = 'FeeReport with id [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class activate_errors:
  FEE_REPORT_ID_NOT_INCLUDED = FeeReportIDNotIncludedError
  FEE_REPORT_DOES_NOT_EXIST = FeeReportDoesNotExistError

class delete_errors:
  FEE_REPORT_ID_NOT_INCLUDED = FeeReportIDNotIncludedError
  FEE_REPORT_DOES_NOT_EXIST = FeeReportDoesNotExistError

class get_errors:
  FEE_REPORT_DOES_NOT_EXIST = FeeReportDoesNotExistError
