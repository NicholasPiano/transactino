
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import AnnouncementModelMethodsSchema
from .instances import AnnouncementInstancesClosedSchema

class AnnouncementModelSchema(ModelSchema):
  def __init__(self, Model, mode=None):
    super().__init__(
      Model,
      mode=mode,
      description=None,
    )
    self.children = {
      schema_constants.METHODS: AnnouncementModelMethodsSchema(Model, mode=mode),
      schema_constants.INSTANCES: AnnouncementInstancesClosedSchema(Model, mode=mode),
    }
