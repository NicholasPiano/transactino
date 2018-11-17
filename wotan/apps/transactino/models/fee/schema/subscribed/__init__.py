
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .instances import FeeReportInstancesClosedSchema
from .methods import FeeReportSubscribedModelMethodsSchema

class FeeReportSubscribedModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children = {
      schema_constants.METHODS: FeeReportSubscribedModelMethodsSchema(Model),
      schema_constants.INSTANCES: FeeReportInstancesClosedSchema(Model, mode=mode),
    }
