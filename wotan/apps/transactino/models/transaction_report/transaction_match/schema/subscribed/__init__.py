
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import TransactionMatchSubscribedModelMethodsSchema

class TransactionMatchSubscribedModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      Model,
      mode=mode,
      **kwargs,
      description=(
        'The schema for the TransactionMatch model. Instances of this model store'
        ' details of successful matches based on the conditions of their parent'
        ' TransactionReport objects.'
      ),
    )
    self.children = {
      schema_constants.METHODS: TransactionMatchSubscribedModelMethodsSchema(Model),
      schema_constants.INSTANCES: self.children[schema_constants.INSTANCES],
    }
