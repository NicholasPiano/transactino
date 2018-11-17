
from util.api import Error

class UniformInclusiveError(Error):
  code = '005'
  name = 'uniform_attribute_inclusive'
  description = 'Attribute keys must be all inclusive or exclusive'

class model_schema_errors:
  UNIFORM_INCLUSIVE = UniformInclusiveError
