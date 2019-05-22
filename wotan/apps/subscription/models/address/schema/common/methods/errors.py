
from util.api import Error

class AddressIdNotIncludedError(Error):
  code = '11be5a9e489745e996de6fb991cdcf85'
  name = 'address_id_not_included'
  description = 'The Address ID must be included in the request'

class AddressDoesNotExistError(Error):
  code = 'e30be0ce51604fefabfa20eaa701a95a'
  name = 'address_does_not_exist'
  description = 'The Address does not exist'
  description_with_arguments = 'The Address with ID [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class get_errors:
  ADDRESS_ID_NOT_INCLUDED = AddressIdNotIncludedError
  ADDRESS_DOES_NOT_EXIST = AddressDoesNotExistError
