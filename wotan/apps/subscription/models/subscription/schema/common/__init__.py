
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .....constants import mode_constants
from .methods import SubscriptionModelMethodsSchema
from .instances import SubscriptionInstancesClosedSchema

class SubscriptionModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children = {
      schema_constants.METHODS: SubscriptionModelMethodsSchema(),
      schema_constants.INSTANCES: SubscriptionInstancesClosedSchema(Model, mode=mode),
    }
