
from util.api import Schema, StructureSchema, map_type

class InstanceAttributeSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='Non-relationship attributes of the model instance',
      children={
        attribute_field.name: Schema(
          types=map_type(attribute_field.get_internal_type())
        )
        for attribute_field
        in self.model.objects.attributes(mode=mode)
      },
    )
