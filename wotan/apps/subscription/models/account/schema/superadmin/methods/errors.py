
from util.api import Error

class AccountIdNotIncludedError(Error):
  code = '1032'
  name = 'account_id_not_included'
  description = 'The account ID must be included'

class lock_errors:
  ACCOUNT_ID_NOT_INCLUDED = AccountIdNotIncludedError
