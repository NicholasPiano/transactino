
from util.api import Error

class TransactionReportDoesNotExistError(Error):
  code = 'f6a8f08cf10143509ef45f377dcecfad'
  name = 'transaction_report_does_not_exist'
  description = 'TransactionReport does not exist'
  description_with_arguments = 'TransactionReport with id [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class TransactionReportIDNotIncludedError(Error):
  code = '66567462bbbd4d84b5ee1b5eda5ef717'
  name = 'transaction_report_id_not_included'
  description = 'TransactionReport ID must be included'

class TargetAddressNotIncludedError(Error):
  code = 'a160fcbb91c2494dac5006052b55f7c3'
  name = 'target_address_not_included'
  description = 'Target address must be included'

class EqualUsedWithRangeError(Error):
  code = 'a81ecc72b1594967a6839f250c8a023e'
  name = 'equal_used_with_range'
  description = (
    'The property "value_equal_to" cannot be used in conjunction with'
    ' "value_less_than" or "value_greater_than".'
  )

class EqualOrRangeNotIncludedError(Error):
  code = '6dd6e650c583490396af21058aa45d10'
  name = 'equal_or_range_not_included'
  description = (
    'One of "value_equal_to", "value_less_than", or "value_greater_than"'
    ' must be included.'
  )

class InvalidValueRangeError(Error):
  code = '0b111811751c46c09637b056ce2b21be'
  name = 'invalid_value_range'
  description = 'The value range is invalid'
  description_with_arguments = 'The lower bound for the value ({}) is greater than the upper bound ({})'

  def __init__(self, lower_bound=None, upper_bound=None):
    self.description = (
      self.description_with_arguments.format(lower_bound, upper_bound)
      if lower_bound is not None and upper_bound is not None
      else self.description
    )

class activate_errors:
  TRANSACTION_REPORT_ID_NOT_INCLUDED = TransactionReportIDNotIncludedError
  TRANSACTION_REPORT_DOES_NOT_EXIST = TransactionReportDoesNotExistError

class create_errors:
  TARGET_ADDRESS_NOT_INCLUDED = TargetAddressNotIncludedError
  EQUAL_USED_WITH_RANGE = EqualUsedWithRangeError
  EQUAL_OR_RANGE_NOT_INCLUDED = EqualOrRangeNotIncludedError
  INVALID_VALUE_RANGE = InvalidValueRangeError

class delete_errors:
  TRANSACTION_REPORT_ID_NOT_INCLUDED = TransactionReportIDNotIncludedError
  TRANSACTION_REPORT_DOES_NOT_EXIST = TransactionReportDoesNotExistError

class get_errors:
  TRANSACTION_REPORT_DOES_NOT_EXIST = TransactionReportDoesNotExistError
