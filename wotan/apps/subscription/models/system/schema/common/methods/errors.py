
from util.api import Error

class SystemGetTakesNoArgumentsError(Error):
  code = '436f9f34886c43a2b4bdc7002b6122af'
  name = 'system_get_takes_no_arguments'
  description = 'System get takes no arguments'

class NoSystemError(Error):
  code = '59ca02f3f8a744bd89aed124a2a0530d'
  name = 'no_system'
  description = 'No active system identity'

class get_errors:
  SYSTEM_GET_TAKES_NO_ARGUMENTS = SystemGetTakesNoArgumentsError
  NO_SYSTEM = NoSystemError
