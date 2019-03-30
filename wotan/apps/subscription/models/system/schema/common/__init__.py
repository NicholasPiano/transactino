
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import SystemModelMethodsSchema
from .instances import SystemInstancesClosedSchema

class SystemModelSchema(ModelSchema):
  def __init__(self, Model, mode=None):
    super().__init__(
      Model,
      mode=mode,
      description=(
        'The schema for the System model. This model'
        ' stores information about the identity of the system'
        ' used to verify challenges made to user identities.'
        ' Any information signed by this identity comes from the'
        ' system itself.'
      ),
    )
    self.children = {
      schema_constants.METHODS: SystemModelMethodsSchema(Model, mode=mode),
      schema_constants.INSTANCES: SystemInstancesClosedSchema(Model, mode=mode),
    }
