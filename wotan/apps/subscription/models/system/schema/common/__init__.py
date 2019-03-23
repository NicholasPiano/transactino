
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import SystemModelMethodsSchema
from .instances import SystemInstancesClosedSchema

class SystemModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children = {
      schema_constants.METHODS: SystemModelMethodsSchema(Model, mode=mode),
      schema_constants.INSTANCES: SystemInstancesClosedSchema(Model, mode=mode),
    }
