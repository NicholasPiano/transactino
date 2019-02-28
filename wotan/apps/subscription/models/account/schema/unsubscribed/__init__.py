
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .....constants import mode_constants
from .methods import AccountUnsubscribedModelMethodsSchema

class AccountUnsubscribedModelSchema(ModelSchema):
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
      schema_constants.METHODS: AccountUnsubscribedModelMethodsSchema(Model),
    }
