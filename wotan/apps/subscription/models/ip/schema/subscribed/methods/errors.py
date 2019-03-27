
from util.api import Error

class ValueNotIncludedError(Error):
  code = '10102'
  name = 'value_not_included'
  description = 'Value must be included'

class IPAlreadyBoundError(Error):
  code = '10091'
  name = 'ip_already_bound'
  description = 'IP Address has already been bound to an account'
  description_with_arguments = 'IP Address with value [{}] has already been bound to an account'

  def __init__(self, value=None):
    self.description = (
      self.description_with_arguments.format(value)
      if value is not None
      else self.description
    )

class create_errors:
  VALUE_NOT_INCLUDED = ValueNotIncludedError
  IP_ALREADY_BOUND = IPAlreadyBoundError

class IpIdNotIncludedError(Error):
  code = '10091'
  name = 'ip_id_not_included'
  description = 'IP ID must be included'

class IPDoesNotExistError(Error):
  code = '1009'
  name = 'ip_does_not_exist'
  description = 'IP Address does not exist'
  description_with_arguments = 'IP Address with id [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class delete_errors:
  IP_ID_NOT_INCLUDED = IpIdNotIncludedError
  IP_DOES_NOT_EXIST = IPDoesNotExistError

class IPGetTakesNoArgumentsError(Error):
  code = '1010'
  name = 'ip_get_takes_no_arguments'
  description = 'IP Address get takes no arguments'

class get_errors:
  IP_GET_TAKES_NO_ARGUMENTS = IPGetTakesNoArgumentsError
