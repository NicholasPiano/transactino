
from util.api import StructureSchema

from apps.base.schema.methods.constants import method_constants
from apps.base.schema.methods.filter import FilterSchema
from apps.base.schema.methods.get import GetSchema

from ......schema.methods.set import SetSchemaWithChallenge
from .constants import set_constants, account_superadmin_method_constants
from .lock import AccountSuperadminLockSchema

class AccountSuperadminModelMethodsSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(
      **kwargs,
      description='',
      children={
        method_constants.FILTER: FilterSchema(Model),
        method_constants.GET: GetSchema(Model),
        method_constants.SET: SetSchemaWithChallenge(Model, origin=set_constants.ORIGIN),
        account_superadmin_method_constants.LOCK: AccountSuperadminLockSchema(Model),
      },
    )
