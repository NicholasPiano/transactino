
from apps.base.schema.methods import ModelMethodsSchema
from apps.base.schema.methods.constants import method_constants

from .constants import fee_report_subscribed_method_constants
from .create import FeeReportCreateSchema
from .delete import FeeReportDeleteSchema
from .get import FeeReportGetSchema
from .activate import FeeReportActivateSchema

class FeeReportSubscribedModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      method_constants.CREATE: FeeReportCreateSchema(Model),
      method_constants.DELETE: FeeReportDeleteSchema(Model),
      method_constants.GET: FeeReportGetSchema(Model),
      fee_report_subscribed_method_constants.ACTIVATE: FeeReportActivateSchema(Model),
    }
