
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import AccountSubscribedModelMethodsSchema

class AccountSubscribedModelSchema(ModelSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children.update({
      schema_constants.METHODS: AccountSubscribedModelMethodsSchema(Model),
    })
