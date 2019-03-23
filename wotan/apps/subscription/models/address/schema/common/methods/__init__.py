
from apps.base.schema.methods import ModelMethodsSchema
from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants

from ......constants import mode_constants
from .get import AddressGetSchema

class AddressModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      method_constants.GET: AddressGetSchema(Model),
    }
