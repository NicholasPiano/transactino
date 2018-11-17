
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import IPSubscribedModelMethodsSchema
from .instances import IPInstancesClosedSchema

class IPSubscribedModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children = {
      schema_constants.METHODS: IPSubscribedModelMethodsSchema(Model),
      schema_constants.INSTANCES: IPInstancesClosedSchema(Model, mode=mode),
    }
