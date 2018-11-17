
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
)

from ..constants import schema_constants
from .base import ResponseWithInternalQuerySet
from .errors import create_errors

class PropertyResponse(StructureResponse):
  def get_properties(self):
    if not self.has_errors() and not self.is_empty:
      return self.render()
    return {}

class PropertySchema(StructureSchema):
  default_response = PropertyResponse

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        create_errors.NON_NULLABLE_NOT_INCLUDED(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)
    non_nullable_not_included = self.non_nullable - payload.keys()
    if non_nullable_not_included:
      self.active_response.add_error(create_errors.NON_NULLABLE_NOT_INCLUDED(not_included=non_nullable_not_included))
      return False

    return passes_pre_response_checks

class AttributesCreateSchema(PropertySchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(**kwargs)
    self.non_nullable = {
      attribute.name
      for attribute in Model.objects.attributes(mode=mode)
      if (
        attribute.editable
        and not attribute.has_default()
        and not attribute.null
      )
    }
    self.children = {
      attribute.name: Schema(
        description=str(attribute.verbose_name),
        types=map_type(attribute.get_internal_type()),
      )
      for attribute in Model.objects.attributes(mode=mode)
      if attribute.editable
    }

class RelationshipsCreateSchema(PropertySchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(**kwargs)
    self.non_nullable = {
      relationship.name
      for relationship in Model.objects.relationships(mode=mode)
      if (
        relationship.editable
        and not relationship.has_default()
        and not relationship.null
        and not relationship.one_to_many
        and not relationship.many_to_many
      )
    }
    self.children = {
      relationship.name: Schema(
        description=relationship.name,
        types=(
          types.UUID()
          if relationship.one_to_one or relationship.many_to_one
          else types.ARRAY()
        ),
      )
      for relationship in Model.objects.relationships(mode=mode)
      if relationship.editable
    }

class PrototypeResponse(StructureResponse):
  def __init__(self, *args):
    super().__init__(*args)
    self._id = None

  def set_id(self, id):
    self._id = id

  def get_id(self):
    return self._id

  def get_prototype(self):
    if not self.has_errors():
      attributes_response = self.force_get_child(schema_constants.ATTRIBUTES)
      relationships_response = self.force_get_child(schema_constants.RELATIONSHIPS)

      attributes = attributes_response.get_properties()
      relationships = relationships_response.get_properties()

      prototype = {}
      for attribute_name, attribute in attributes.items():
        prototype.update({attribute_name: attribute})

      for relationship_name, relationship in relationships.items():
        prototype.update({relationship_name: relationship})

      return prototype

class PrototypeSchema(TemplateSchema, StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=PrototypeResponse,
      children={
        schema_constants.ATTRIBUTES: AttributesCreateSchema(Model, mode=mode),
        schema_constants.RELATIONSHIPS: RelationshipsCreateSchema(Model, mode=mode),
      },
    )
    self.non_nullable = {
      child_key
      for child_key, child in self.children.items()
      if child.non_nullable
    }

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        create_errors.MUST_CONTAIN_ALL_NON_NULLABLE(),
      },
    )

  def passes_pre_response_checks(self, key, payload, context):
    missing_non_nullable = self.non_nullable - payload.keys()
    if missing_non_nullable:
      self.active_response.add_error(
        create_errors.MUST_CONTAIN_ALL_NON_NULLABLE(must_contain=missing_non_nullable),
      )
      return False

    return super().passes_pre_response_checks(key, payload, context)

  def responds_to_valid_payload(self, key, payload, context):
    super().responds_to_valid_payload(key, payload, context)

    prototype = self.active_response.get_prototype()

    add_after_creation = {}
    modified_kwargs = {}

    for property_key, property in prototype.items():
      field = self.model._meta.get_field(property_key)
      if field.is_relation:
        if field.one_to_one or field.many_to_one:
          related_object = field.related_model.objects.get(id=property)
          modified_kwargs.update({
            property_key: related_object,
          })
        elif field.one_to_many or field.many_to_many:
          related_objects = field.related_model.objects.filter(id__in=property)
          add_after_creation.update({
            property_key: related_objects,
          })
      else:
        modified_kwargs.update({property_key: property})

    created = self.model.objects.create(**modified_kwargs)

    for property_key, property in add_after_creation.items():
      for related_object in property:
        relationship = getattr(created, property_key)
        relationship.add(related_object)

    self.active_response.set_id(created._id)

class CreateClientResponse(IndexedResponse, ResponseWithInternalQuerySet):
  pass

class CreateClientSchema(IndexedSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=CreateClientResponse,
      template=TemplateSchema(types=types.UUID()),
    )

class CreateSchema(IndexedSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      template=PrototypeSchema(Model, mode=mode),
      client=CreateClientSchema(),
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    temporary_ids = {}
    for prototype_temporary_id, prototype_response in self.active_response.children.items():
      created_id = prototype_response.get_id()
      temporary_ids.update({
        prototype_temporary_id: created_id,
      })

    full_queryset = self.model.objects.filter(id__in=temporary_ids.values())

    if full_queryset:
      self.active_response = self.client.respond(payload=temporary_ids)
      self.active_response.add_internal_queryset(full_queryset)
