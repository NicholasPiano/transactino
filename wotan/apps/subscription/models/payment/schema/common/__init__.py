
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import PaymentModelMethodsSchema

class PaymentModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      Model,
      mode=mode,
      **kwargs,
      description=(
        'The schema for the Payment model. Payments store details of bitcoin'
        ' transactions that must be closed before an action can be completed.'
      ),
    )
    self.children = {
      schema_constants.METHODS: PaymentModelMethodsSchema(Model),
      schema_constants.INSTANCES: self.children[schema_constants.INSTANCES],
    }
