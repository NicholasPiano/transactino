
from apps.base.schema.methods import ModelMethodsSchema
from apps.base.schema.constants import schema_constants

from ......constants import mode_constants
from .constants import account_unsubscribed_method_constants
from .verify import AccountVerifySchema
from .delete import AccountDeleteSchema

class AccountUnsubscribedModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      account_unsubscribed_method_constants.VERIFY: AccountVerifySchema(),
      account_unsubscribed_method_constants.DELETE: AccountDeleteSchema(),
    }
