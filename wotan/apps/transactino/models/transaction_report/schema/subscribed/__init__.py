
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .instances import TransactionReportInstancesClosedSchema
from .methods import TransactionReportSubscribedModelMethodsSchema

class TransactionReportSubscribedModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      Model,
      mode=mode,
      **kwargs,
      description=(
        'The schema for the TransactionReport model. Instances of this model store'
        ' match conditions for transactions on the Blockchain and references to'
        ' successful matches.'
      ),
    )
    self.children = {
      schema_constants.METHODS: TransactionReportSubscribedModelMethodsSchema(Model),
      schema_constants.INSTANCES: TransactionReportInstancesClosedSchema(Model, mode=mode),
    }
