
from apps.base.schema.methods import ModelMethodsSchema
from apps.base.schema.methods.constants import method_constants

from .create import IPCreateSchema
from .delete import IPDeleteSchema
from .get import IPGetSchema

class IPSubscribedModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      method_constants.CREATE: IPCreateSchema(Model),
      method_constants.DELETE: IPDeleteSchema(Model),
      method_constants.GET: IPGetSchema(Model),
    }
