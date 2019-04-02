
from apps.base.schema.methods import ModelMethodsSchema
from apps.base.schema.methods.constants import method_constants

from .constants import transaction_match_subscribed_method_constants
from .get import TransactionMatchGetSchema
from .dismiss import TransactionMatchDismissSchema

class TransactionMatchSubscribedModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      method_constants.GET: TransactionMatchGetSchema(Model),
      transaction_match_subscribed_method_constants.DISMISS: TransactionMatchDismissSchema(Model),
    }
