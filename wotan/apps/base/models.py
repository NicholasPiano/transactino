
import uuid

from django.db import models

from util.api import Schema, StructureSchema, Error, constants

from .constants import (
  APP_LABEL,
  query_directives,
  is_valid_query_directive,
  model_fields,
  mock_model_constants,
  mock_model_fields,
)
from .schema import schema_constants, ModelSchema
from .schema.methods.constants import filter_constants

class Manager(models.Manager):
  use_for_related_fields = True

  def attributes(self, mode=None):
    return [
      field
      for field in self.model._meta.get_fields()
      if (
        not field.is_relation
        and field.name != model_fields.ID
      )
    ]

  def relationships(self, mode=None):
    return [
      field
      for field in self.model._meta.get_fields()
      if (
        field.is_relation
        or (
          field.auto_created
          and not field.concrete
        )
      )
    ]

  def serialize(self, instance, attributes=None, relationships=None, mode=None):
    return {
      schema_constants.ATTRIBUTES: self.serialize_attributes(
        instance,
        attributes=attributes,
        mode=mode,
      ),
      schema_constants.RELATIONSHIPS: self.serialize_relationships(
        instance,
        relationships=relationships,
        mode=mode,
      ),
    }

  def serialize_attributes(self, instance, attributes=None, mode=None):
    return {
      attribute_field.name: (
        str(getattr(instance, attribute_field.name))
        if attribute_field.get_internal_type() not in constants.PLAIN_TYPES
        else getattr(instance, attribute_field.name)
      )
      for attribute_field
      in self.attributes(mode=mode)
      if attributes is None or attribute_field.name in attributes
    }

  def serialize_relationships(self, instance, relationships=None, mode=None):
    return {
      relationship_field.name: (
        (
          getattr(instance, relationship_field.name)._ref
          if getattr(instance, relationship_field.name) is not None
          else constants.NULL
        )
        if relationship_field.one_to_one or relationship_field.many_to_one
        else [
          related_object._ref
          for related_object
          in getattr(instance, relationship_field.name).all()
        ]
      )
      for relationship_field
      in self.relationships(mode=mode)
      if relationships is None or relationship_field.name in relationships
    }

  def schema(self, mode=None):
    return ModelSchema(self.model, mode=mode)

  def get(self, **kwargs):
    filtered = super().filter(**kwargs)
    if filtered.exists():
      return filtered[0]
    return None

  def filter(self, *args, **kwargs):
    return super().filter(*args, **kwargs)

  def query_check(self, key):
    tokens = key.split(query_directives.JOIN)
    field_name, rest_of_tokens = tokens[0], tokens[1:]
    field = self.model._meta.get_field(field_name)

    anomalies = []
    if field.is_relation:
      anomalies.extend(
        field.related_model.objects.query_check(
          query_directives.JOIN.join(rest_of_tokens),
        ),
      )
    else:
      directive = query_directives.JOIN.join(rest_of_tokens)
      if not is_valid_query_directive(directive):
        anomalies.append((
          self.model.__name__,
          field_name,
          directive,
        ))

    return anomalies

class Model(models.Model):
  objects = Manager()

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Date created')

  class Meta:
    abstract = True

  @property
  def _id(self):
    return self.id.hex

  @property
  def _ref(self):
    return '{}.{}'.format(self.__class__.__name__, self._id)

class MockParentModel(Model):
  name = models.CharField(max_length=255)

  class Meta:
    app_label = APP_LABEL

class MockModel(Model):
  parent = models.ForeignKey(
    mock_model_constants.PARENT_RELATED_MODEL,
    related_name=mock_model_constants.PARENT_RELATED_NAME,
    on_delete=models.CASCADE,
    null=True,
  )
  parent_non_nullable = models.ForeignKey(
    mock_model_constants.PARENT_NON_NULLABLE_RELATED_MODEL,
    related_name=mock_model_constants.PARENT_NON_NULLABLE_RELATED_NAME,
    on_delete=models.CASCADE,
  )
  under = models.ManyToManyField(
    mock_model_constants.UNDER_RELATED_MODEL,
    related_name=mock_model_constants.UNDER_RELATED_NAME,
    symmetrical=False,
  )
  name = models.CharField(max_length=255)

  class Meta:
    app_label = APP_LABEL
