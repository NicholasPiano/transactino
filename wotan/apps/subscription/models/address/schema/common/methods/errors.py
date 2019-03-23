
from util.api import Error

class AddressGetTakesNoArgumentsError(Error):
  code = '7252'
  name = 'address_get_takes_no_arguments'
  description = 'Address get takes no arguments'

class NoAddressError(Error):
  code = '9223'
  name = 'no_address'
  description = 'No active address for making payments'

class get_errors:
  ADDRESS_GET_TAKES_NO_ARGUMENTS = AddressGetTakesNoArgumentsError
  NO_ADDRESS = NoAddressError
