
from util.api import Error

class SystemGetTakesNoArgumentsError(Error):
  code = '72521'
  name = 'system_get_takes_no_arguments'
  description = 'System get takes no arguments'

class NoSystemError(Error):
  code = '92232'
  name = 'no_system'
  description = 'No active system identity'

class get_errors:
  SYSTEM_GET_TAKES_NO_ARGUMENTS = SystemGetTakesNoArgumentsError
  NO_SYSTEM = NoSystemError
