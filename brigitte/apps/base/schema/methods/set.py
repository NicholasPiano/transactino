
from util.api import (
  Schema, StructureSchema, ArraySchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
)

from ..constants import schema_constants
from .base import ResponseWithInternalQuerySet
from .constants import set_constants
from .errors import set_errors, method_errors

class PropertyResponse(Response):
  def __init__(self, *args):
    self.property = None
    super().__init__(*args)

  def set_property(self, property):
    self.property = property

  def get_property(self):
    return self.property or self.value

  def should_render(self):
    return self.has_errors()

class NullableSchema(StructureSchema):
  def __init__(self, field, **kwargs):
    self.field = field
    super().__init__(
      **kwargs,
      client=Schema(response=PropertyResponse),
      children={
        set_constants.NULL: Schema(types=types.BOOLEAN()),
      }
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        set_errors.NULLABLE_MUST_CONTAIN_KEY(),
        set_errors.NULLABLE_MUST_BE_TRUE(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if set_constants.NULL not in payload:
      self.active_response.add_error(set_errors.NULLABLE_MUST_CONTAIN_KEY(field=self.field.name))
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    null_response = self.active_response.get_child(set_constants.NULL)
    if not null_response.value:
      self.active_response.add_error(set_errors.NULLABLE_MUST_BE_TRUE(field=self.field.name))
      return

    self.active_response = self.client.get_response()

class PropertiesResponse(StructureResponse):
  def get_properties(self):
    if not self.has_errors():
      return {
        property: property_response.get_property()
        for property, property_response
        in self.children.items()
      }

class AttributeSchema(Schema):
  def __init__(self, attribute, **kwargs):
    attribute_schema_types = [map_type(attribute.get_internal_type())]
    if attribute.null:
      attribute_schema_types.append(
        types.STRUCTURE(
          schema=NullableSchema(attribute),
        ),
      )

    super().__init__(
      **kwargs,
      description=str(attribute.verbose_name),
      response=PropertyResponse,
      types=attribute_schema_types,
    )

class AttributesSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      **kwargs,
      response=PropertiesResponse,
      children={
        attribute.name: AttributeSchema(attribute)
        for attribute in Model.objects.attributes(mode=mode)
        if attribute.editable
      },
    )

class SingleSchema(Schema):
  def __init__(self, relationship, **kwargs):
    self.relationship = relationship
    super().__init__(
      **kwargs,
      types=types.UUID(),
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        method_errors.DOES_NOT_EXIST(),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    instance = self.relationship.related_model.objects.get(id=payload)

    if instance is None:
      self.active_response.add_error(method_errors.DOES_NOT_EXIST(id=payload))
      return

class ManySchema(ArraySchema):
  def __init__(self, relationship, **kwargs):
    super().__init__(
      **kwargs,
      client=Schema(response=PropertyResponse),
      template=SingleSchema(relationship),
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    many = self.active_response.render()
    self.active_response = self.client.get_response()
    self.active_response.set_property(many)

class RelationshipManySchema(StructureSchema):
  def __init__(self, relationship, **kwargs):
    super().__init__(
      **kwargs,
      client=Schema(response=PropertyResponse),
      children={
        set_constants.ADD: ManySchema(relationship),
        set_constants.REMOVE: ManySchema(relationship),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    add_response = self.active_response.get_child(set_constants.ADD)
    add = add_response.get_property() if add_response is not None else []

    remove_response = self.active_response.get_child(set_constants.REMOVE)
    remove = remove_response.get_property() if remove_response is not None else []

    self.active_response = self.client.get_response()
    self.active_response.set_property({
      set_constants.ADD: add,
      set_constants.REMOVE: remove,
    })

class RelationshipSchema(Schema):
  def __init__(self, relationship, **kwargs):
    self.relationship = relationship

    if relationship.one_to_one or relationship.many_to_one:
      relationship_schema_types = [types.UUID()]
      if relationship.null:
        relationship_schema_types.append(
          types.STRUCTURE(
            schema=NullableSchema(relationship),
          ),
        )
    else:
      relationship_schema_types = types.STRUCTURE(
        schema=RelationshipManySchema(relationship),
      )

    super().__init__(
      **kwargs,
      description=relationship.name,
      response=PropertyResponse,
      types=relationship_schema_types,
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        method_errors.DOES_NOT_EXIST(),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    instance = self.relationship.related_model.objects.get(id=payload)

    if instance is None:
      self.active_response.add_error(method_errors.DOES_NOT_EXIST(id=payload))
      return

class RelationshipsSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      **kwargs,
      response=PropertiesResponse,
      children={
        relationship.name: RelationshipSchema(relationship)
        for relationship in Model.objects.relationships(mode=mode)
      },
    )

class PrototypeResponse(StructureResponse):
  def get_prototype(self):
    if not self.has_errors():
      attributes_response = self.force_get_child(schema_constants.ATTRIBUTES)
      relationships_response = self.force_get_child(schema_constants.RELATIONSHIPS)

      attributes = attributes_response.get_properties()
      relationships = relationships_response.get_properties()

      if attributes or relationships:
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
      client=Schema(types=types.BOOLEAN()),
      children={
        schema_constants.ATTRIBUTES: AttributesSchema(Model, mode=mode),
        schema_constants.RELATIONSHIPS: RelationshipsSchema(Model, mode=mode),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        method_errors.DOES_NOT_EXIST(),
      },
    )

  def responds_to_valid_payload(self, key, payload, context):
    super().responds_to_valid_payload(key, payload, context)

    instance = self.model.objects.get(id=key)

    if instance is None:
      self.active_response.add_error(method_errors.DOES_NOT_EXIST(id=key))
      return

    prototype = self.active_response.get_prototype()

    for property_key, property in prototype.items():
      field = self.model._meta.get_field(property_key)
      if field.is_relation:
        if field.one_to_one or field.many_to_one:
          related_object = field.related_model.objects.get(id=property)
          setattr(instance, property_key, related_object)

        elif field.one_to_many or field.many_to_many:
          related_field = getattr(instance, property_key)

          for related_item_id in property.get(set_constants.ADD):
            related_item = field.related_model.objects.get(id=related_item_id)
            related_field.add(related_item)

          for related_item_id in property.get(set_constants.REMOVE):
            related_item = field.related_model.objects.get(id=related_item_id)
            related_field.remove(related_item)

      else:
        setattr(instance, property_key, property)

    instance.save()

    self.active_response = self.client.respond(payload=True)

class SetResponse(IndexedResponse, ResponseWithInternalQuerySet):
  pass

class SetSchema(IndexedSchema):
  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=SetResponse,
      template=PrototypeSchema(Model, mode=mode),
      client=Schema(),
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    full_queryset = self.model.objects.filter(id__in=self.active_response.children.keys())

    if full_queryset:
      self.active_response.add_internal_queryset(full_queryset)
