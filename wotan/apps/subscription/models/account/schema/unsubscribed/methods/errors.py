
from util.api import Error

class AccountVerifyTakesNoArgumentsError(Error):
  code = '725'
  name = 'account_verify_takes_no_arguments'
  description = 'Account verify takes no arguments'

class AccountAlreadyVerifiedError(Error):
  code = '726'
  name = 'account_already_verified'
  description = 'This account has already been verified'

class verify_errors:
  ACCOUNT_ALREADY_VERIFIED = AccountAlreadyVerifiedError
  ACCOUNT_VERIFY_TAKES_NO_ARGUMENTS = AccountVerifyTakesNoArgumentsError

class AccountDeleteTakesNoArgumentsError(Error):
  code = '727'
  name = 'account_delete_takes_no_arguments'
  description = 'Account delete takes no arguments'

class delete_errors:
  ACCOUNT_DELETE_TAKES_NO_ARGUMENTS = AccountDeleteTakesNoArgumentsError
