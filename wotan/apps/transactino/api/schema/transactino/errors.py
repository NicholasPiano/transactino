
from util.api import Error

class NoActiveSystemError(Error):
  code = 'c9f06acd7d85485985460cc653dd2e95'
  name = 'no_active_system'
  description = 'No active system is online to receive requests'

class transactino_errors:
  NO_ACTIVE_SYSTEM = NoActiveSystemError
