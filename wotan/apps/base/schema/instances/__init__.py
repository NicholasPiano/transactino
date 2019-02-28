
from util.api import (
  Schema, ClosedSchema, StructureSchema, IndexedSchema,
  StructureResponse, IndexedResponse,
  types,
  errors,
  constants,
)

from ..constants import schema_constants
from .attributes import InstanceAttributeSchema
from .relationships import InstanceRelationshipSchema

class InstanceSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    self.mode = mode
    super().__init__(
      **kwargs,
      description=(
        'The schema for reporting a single instance of the {} model.'
      ).format(
        Model.__name__,
      ),
      children={
        schema_constants.ATTRIBUTES: InstanceAttributeSchema(Model, mode=mode),
        schema_constants.RELATIONSHIPS: InstanceRelationshipSchema(Model, mode=mode),
      },
    )

  def response_from_model_instance(self, instance, attributes=None, relationships=None):
    return self.respond(
      payload=self.model.objects.serialize(
        instance,
        attributes=attributes,
        relationships=relationships,
        mode=self.mode,
      ),
    )

class InstancesResponse(IndexedResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.attributes = None
    self.relationships = None

  def add_attributes(self, attributes):
    self.attributes = attributes

  def add_relationships(self, relationships):
    self.relationships = relationships

  def add_instances(self, instances):
    for instance in instances:
      self.add_child(
        instance._id,
        self.template_schema.response_from_model_instance(
          instance,
          attributes=self.attributes,
          relationships=self.relationships,
        )
      )

class InstancesSchema(IndexedSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      **kwargs,
      response=InstancesResponse,
      template=InstanceSchema(Model, mode=mode),
    )

class InstancesClosedSchema(ClosedSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for reporting details of instances of the'
        ' {} model. This schema takes no input and does not trigger'
        ' any methods or any interaction with the API.'
      ).format(
        Model.__name__,
      ),
      client=InstancesSchema(Model, mode=mode),
    )
