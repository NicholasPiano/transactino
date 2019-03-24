
from apps.base.schema.methods import ModelMethodsSchema
from apps.base.schema.methods.constants import method_constants

from .constants import transaction_report_subscribed_method_constants
from .create import TransactionReportCreateSchema
from .delete import TransactionReportDeleteSchema
from .get import TransactionReportGetSchema
from .activate import TransactionReportActivateSchema

class TransactionReportSubscribedModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      method_constants.CREATE: TransactionReportCreateSchema(Model),
      method_constants.DELETE: TransactionReportDeleteSchema(Model),
      method_constants.GET: TransactionReportGetSchema(Model),
      transaction_report_subscribed_method_constants.ACTIVATE: TransactionReportActivateSchema(Model),
    }
