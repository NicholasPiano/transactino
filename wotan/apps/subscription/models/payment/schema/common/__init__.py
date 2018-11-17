
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import PaymentModelMethodsSchema
from .instances import PaymentInstancesClosedSchema

class PaymentModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children = {
      schema_constants.METHODS: PaymentModelMethodsSchema(Model),
      schema_constants.INSTANCES: PaymentInstancesClosedSchema(Model, mode=mode),
    }
