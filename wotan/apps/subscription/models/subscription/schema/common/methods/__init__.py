
from util.api import StructureSchema

from apps.base.schema.methods.constants import method_constants

from .constants import subscription_method_constants
from .create import SubscriptionCreateSchema
from .activate import SubscriptionActivateSchema
from .get import SubscriptionGetSchema

class SubscriptionModelMethodsSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      method_constants.CREATE: SubscriptionCreateSchema(),
      subscription_method_constants.ACTIVATE: SubscriptionActivateSchema(),
      method_constants.GET: SubscriptionGetSchema(),
    }
