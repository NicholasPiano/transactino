
from util.api import Error

class InvalidPublicKeyError(Error):
  code = '120'
  name = 'invalid_public_key'
  description = 'Public key must be a valid GPG public key'

class PublicKeyNotIncludedError(Error):
  code = '122'
  name = 'public_key_not_included'
  description = 'Public key must be included'

class AccountAlreadyExistsError(Error):
  code = '123'
  name = 'account_already_exists'
  description = 'An account with this public key already exists'

class IPAlreadyExistsError(Error):
  code = '124'
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
