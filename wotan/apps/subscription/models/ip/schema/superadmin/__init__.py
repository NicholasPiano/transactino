
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import IPSuperadminModelMethodsSchema

class IPSuperadminModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children.update({
      schema_constants.METHODS: IPSuperadminModelMethodsSchema(Model, mode=mode),
    })
