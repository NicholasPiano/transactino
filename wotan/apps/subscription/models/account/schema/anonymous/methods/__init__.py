
from apps.base.schema.methods import ModelMethodsSchema, CreateSchema, DeleteSchema
from apps.base.schema.methods.constants import method_constants

from .create import AccountCreateSchema

class AccountAnonymousModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      method_constants.CREATE: AccountCreateSchema(Model),
    }
