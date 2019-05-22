
from util.api import Error

class InvalidPublicKeyError(Error):
  code = '71a90b01d0c24f79bc5a56678ba8a9e9'
  name = 'invalid_public_key'
  description = 'Public key must be a valid GPG public key'

class PublicKeyNotIncludedError(Error):
  code = 'ee6380ea763744c88604d9365aa67cbd'
  name = 'public_key_not_included'
  description = 'Public key must be included'

class AccountAlreadyExistsError(Error):
  code = '2eceb598113843c7b53a447587884605'
  name = 'account_already_exists'
  description = 'An account with this public key already exists'

class IPAlreadyExistsError(Error):
  code = 'c7c6f18827ee4b7791103cd67f2d2970'
  name = 'ip_already_exists'
  description = 'The IP address has already been claimed by another account'
  description_with_arguments = 'The IP address [{}] has already been claimed by another account'

  def __init__(self, ip=None):
    self.description = (
      self.description_with_arguments.format(ip)
      if ip is not None
      else self.description
    )

class account_anonymous_method_errors:
  INVALID_PUBLIC_KEY = InvalidPublicKeyError
  PUBLIC_KEY_NOT_INCLUDED = PublicKeyNotIncludedError
  ACCOUNT_ALREADY_EXISTS = AccountAlreadyExistsError
  IP_ALREADY_EXISTS = IPAlreadyExistsError
