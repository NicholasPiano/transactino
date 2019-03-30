
from util.api import Schema, StructureSchema, StructureResponse, types

class InstanceRelationshipResponse(StructureResponse):
  pass

class InstanceRelationshipSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=InstanceRelationshipResponse,
      description='Relationships on the model instance',
      children={
        relationship_field.name: Schema(
          description=(
            relationship_field.verbose_name
            if hasattr(relationship_field, 'verbose_name')
            else relationship_field.get_related_field().verbose_name
          ),
          types=[
            types.REF(description='A database reference to a single other model instance'),
            types.ARRAY(description='An array of references to multiple other model instances'),
            types.NULL(description='A null value'),
          ],
        )
        for relationship_field
        in self.model.objects.relationships(mode=mode)
      }
    )
