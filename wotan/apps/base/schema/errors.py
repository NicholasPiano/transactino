
from util.api import Error

class UniformInclusiveError(Error):
  code = '0b9c25e0676c4801afa8007dc01fa763'
  name = 'uniform_attribute_inclusive'
  description = 'Attribute keys must be all inclusive or exclusive'

class model_schema_errors:
  UNIFORM_INCLUSIVE = UniformInclusiveError
