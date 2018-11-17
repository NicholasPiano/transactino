
from util.api.schema import StructureSchema

from apps.base.schema.constants import schema_constants

from .....constants import mode_constants
from .methods import AccountAnonymousModelMethodsSchema

class AccountAnonymousModelSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      schema_constants.METHODS: AccountAnonymousModelMethodsSchema(Model),
    }
