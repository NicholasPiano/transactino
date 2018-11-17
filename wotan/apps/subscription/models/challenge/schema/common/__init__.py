
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .....constants import mode_constants
from .methods import ChallengeModelMethodsSchema
from .instances import ChallengeInstancesClosedSchema

class ChallengeModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children = {
      schema_constants.METHODS: ChallengeModelMethodsSchema(Model),
      schema_constants.INSTANCES: ChallengeInstancesClosedSchema(Model, mode=mode),
    }
