
from util.merge import merge
from util.api import Schema, StructureSchema, types, constants

from .constants import schema_constants
from .attributes import AttributeSchema
from .relationships import RelationshipSchema
from .instances import InstancesClosedSchema
from .methods import ModelMethodsSchema

class ModelsSchemaWithExternal(StructureSchema):
  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    models_in_payload = set(self.active_response.children.keys())

    if models_in_payload:
      for model_name in models_in_payload:
        model_response = self.active_response.get_child(model_name)
        methods_response = model_response.get_child(schema_constants.METHODS)

        if methods_response is not None:
          for method_response in methods_response.children.values():
            if hasattr(method_response, schema_constants.EXTERNAL_QUERYSETS):
              for external_queryset in method_response.external_querysets:
                external_model_name = external_queryset.model.__name__
                external_model_response = self.active_response.force_get_child(external_model_name)
                external_model_instances_response = external_model_response.force_get_child(schema_constants.INSTANCES)
                external_model_instances_response.add_instances(external_queryset)

class ModelSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      schema_constants.ATTRIBUTES: AttributeSchema(Model, mode=mode),
      schema_constants.RELATIONSHIPS: RelationshipSchema(Model, mode=mode),
      schema_constants.METHODS: ModelMethodsSchema(Model, mode=mode),
      schema_constants.INSTANCES: InstancesClosedSchema(Model, mode=mode),
    }

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    methods_response = self.active_response.get_child(schema_constants.METHODS)
    methods_internal_instances = []
    if methods_response is not None:
      for methods_child in methods_response.children.values():
        if hasattr(methods_child, schema_constants.INTERNAL_QUERYSET):
          if methods_child.internal_queryset is not None:
            methods_internal_instances.extend(list(methods_child.internal_queryset))

    if methods_internal_instances:
      instances_response = self.active_response.force_get_child(schema_constants.INSTANCES)

      if self.active_response.has_child(schema_constants.ATTRIBUTES):
        attributes_response = self.active_response.get_child(schema_constants.ATTRIBUTES)
        instances_response.add_attributes(attributes_response.get_attributes())

      if self.active_response.has_child(schema_constants.RELATIONSHIPS):
        relationships_response = self.active_response.get_child(schema_constants.RELATIONSHIPS)
        instances_response.add_relationships(relationships_response.get_relationships())

      instances_response.add_instances(methods_internal_instances)
