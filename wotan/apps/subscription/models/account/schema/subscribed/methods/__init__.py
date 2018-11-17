
from util.api import StructureSchema

from .constants import account_subscribed_method_constants
from .lock import AccountSubscribedLockSchema

class AccountSubscribedModelMethodsSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(
      **kwargs,
      description='',
      children={
        account_subscribed_method_constants.LOCK: AccountSubscribedLockSchema(Model),
      },
    )
