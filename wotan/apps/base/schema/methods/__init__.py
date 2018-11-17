
from util.api import StructureSchema

from .constants import method_constants
from .filter import FilterSchema
from .create import CreateSchema
from .delete import DeleteSchema
from .get import GetSchema
from .set import SetSchema

class ModelMethodsSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='Model methods available for {}'.format(Model.__name__),
    )
    self.children = {
      method_constants.FILTER: FilterSchema(Model),
      method_constants.CREATE: CreateSchema(Model, mode=mode),
      method_constants.DELETE: DeleteSchema(Model),
      method_constants.GET: GetSchema(Model),
      method_constants.SET: SetSchema(Model, mode=mode),
    }
