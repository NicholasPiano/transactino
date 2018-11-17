
from util.api import Error

class AccountNotIncludedError(Error):
  code = '1032'
  name = 'account_not_included'
  description = 'The account ID must be included'

class account_superadmin_method_errors:
  ACCOUNT_NOT_INCLUDED = AccountNotIncludedError
