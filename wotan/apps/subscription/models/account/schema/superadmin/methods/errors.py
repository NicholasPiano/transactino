
from util.api import Error

class AccountIdNotIncludedError(Error):
  code = 'a91cb23ac50c4d0bb0785dd203bf05e6'
  name = 'account_id_not_included'
  description = 'The account ID must be included'

class lock_errors:
  ACCOUNT_ID_NOT_INCLUDED = AccountIdNotIncludedError
