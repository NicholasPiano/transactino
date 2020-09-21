
from util.api import Schema, StructureSchema, types, map_type

class InstanceAttributeSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='Non-relationship attributes of the model instance',
      children={
        attribute_field.name: Schema(
          description=attribute_field.verbose_name,
          types=(
            [
              map_type(attribute_field.get_internal_type()),
              types.NULL(),
            ]
            if attribute_field.null
            else map_type(attribute_field.get_internal_type())
          )
        )
        for attribute_field
        in self.model.objects.attributes(mode=mode)
      },
    )
