
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import AddressModelMethodsSchema

class AddressModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      Model,
      mode=mode,
      **kwargs,
      description=(
        'The schema for the Address model'
      ),
    )
    self.children = {
      schema_constants.METHODS: AddressModelMethodsSchema(Model, mode=mode),
      schema_constants.INSTANCES: self.children[schema_constants.INSTANCES],
    }
