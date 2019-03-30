
from apps.base.schema.methods import ModelMethodsSchema
from apps.base.schema.constants import schema_constants

from ......constants import mode_constants
from .constants import announcement_method_constants
from .get import AnnouncementGetSchema

class AnnouncementModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      announcement_method_constants.GET: AnnouncementGetSchema(Model),
    }
