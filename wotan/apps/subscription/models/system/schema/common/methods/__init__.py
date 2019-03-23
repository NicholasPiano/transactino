
from apps.base.schema.methods import ModelMethodsSchema
from apps.base.schema.constants import schema_constants

from ......constants import mode_constants
from .constants import system_method_constants
from .get import SystemGetSchema

class SystemModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      system_method_constants.GET: SystemGetSchema(Model),
    }
