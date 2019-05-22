
from util.api import Error

class AccountVerifyTakesNoArgumentsError(Error):
  code = '63f54b8de5634f9fa8af008233d25137'
  name = 'account_verify_takes_no_arguments'
  description = 'Account verify takes no arguments'

class AccountAlreadyVerifiedError(Error):
  code = '8b6bf0855231485b871b7b15e7df89a4'
  name = 'account_already_verified'
  description = 'This account has already been verified'

class verify_errors:
  ACCOUNT_ALREADY_VERIFIED = AccountAlreadyVerifiedError
  ACCOUNT_VERIFY_TAKES_NO_ARGUMENTS = AccountVerifyTakesNoArgumentsError

class AccountDeleteTakesNoArgumentsError(Error):
  code = 'f075c3658dbb493999154daf0d1a170e'
  name = 'account_delete_takes_no_arguments'
  description = 'Account delete takes no arguments'

class delete_errors:
  ACCOUNT_DELETE_TAKES_NO_ARGUMENTS = AccountDeleteTakesNoArgumentsError
