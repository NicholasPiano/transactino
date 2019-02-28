
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import AccountSubscribedModelMethodsSchema

class AccountSubscribedModelSchema(ModelSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(
      Model,
      **kwargs,
      description=(
        'The schema for the Account model.'
        ' This model controls access to the core'
        ' functionality of the application.'
      )
    )
    self.children = {
      schema_constants.METHODS: AccountSubscribedModelMethodsSchema(Model),
    }
