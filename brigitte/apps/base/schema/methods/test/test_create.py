
import json
import uuid

from django.db import models
from django.test import TestCase

from util.api import (
  Schema, StructureSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from ....models import MockModel, MockParentModel
from ....constants import mock_model_fields
from ...constants import schema_constants
from ..errors import create_errors
from ..create import (
  PropertyResponse,
  PropertySchema,
  AttributesCreateSchema,
  RelationshipsCreateSchema,
  CreateClientResponse,
  CreateClientSchema,
  CreateSchema,
)

class PropertyResponseTestCase(TestCase):
  def setUp(self):
    self.key = 'key'
    self.value = 'value'
    self.schema = StructureSchema(
      response=PropertyResponse,
      children={
        self.key: Schema(),
      },
    )

  def test_response(self):
    payload = {
      self.key: self.value,
    }

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.get_properties(), {
      self.key: self.value,
    })

  def test_with_errors(self):
    payload = {
      self.key + 'error': self.value,
    }

    response = self.schema.respond(payload=payload)

    self.assertFalse(response.get_properties())

  def test_empty(self):
    payload = None

    response = self.schema.respond(payload=payload)

    self.assertFalse(response.get_properties())

class PropertySchemaTestCase(TestCase):
  def setUp(self):
    self.non_nullable_key = 'non-nullable-key'
    self.non_nullable = [
      self.non_nullable_key
    ]
    self.value = 'value'
    self.schema = PropertySchema(
      children={
        self.non_nullable_key: Schema(),
      }
    )
    self.schema.non_nullable = self.non_nullable

  def test_response(self):
    payload = {
      self.non_nullable_key: self.value,
    }

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.render(), {
      self.non_nullable_key: self.value,
    })

  def test_response_without_non_nullable(self):
    payload = {}

    response = self.schema.respond(payload=payload)
    error = create_errors.NON_NULLABLE_NOT_INCLUDED(not_included=[self.non_nullable_key])
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

class TestAttribute():
  def __init__(self, name=None, null=False, editable=True, default=None):
    self.name = name
    self.verbose_name = name
    self.null = null
    self.editable = editable
    self.default = default

  def get_internal_type(self):
    return 'CharField'

  def has_default(self):
    return self.default

class TestAttributeModel():
  attributes = []
  class objects:
    def attributes(mode=None):
      return TestAttributeModel.attributes

class AttributesCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.non_nullable_name = 'non_nullable_name'
    self.nullable_name = 'nullable_name'
    self.non_editable_name = 'non_editable_name'
    self.default = 'default'
    TestAttributeModel.attributes = [
      TestAttribute(name=self.non_nullable_name),
      TestAttribute(name=self.nullable_name, null=True, default=self.default),
      TestAttribute(name=self.non_editable_name, editable=False, default=self.default),
    ]

    self.schema = AttributesCreateSchema(TestAttributeModel)

  def test_exclusions(self):
    self.assertEqual(self.schema.children.keys(), {self.non_nullable_name, self.nullable_name})
    self.assertEqual(self.schema.non_nullable, {self.non_nullable_name})

class TestRelationship():
  def __init__(self,
    name=None,
    null=False,
    one_to_one=False,
    one_to_many=False,
    many_to_many=False,
    many_to_one=False,
    editable=True,
    default=None,
  ):
    self.name = name
    self.verbose_name = name
    self.null = null
    self.one_to_one = one_to_one
    self.one_to_many = one_to_many
    self.many_to_many = many_to_many
    self.many_to_one = many_to_one
    self.editable = editable
    self.default = default

  def get_internal_type(self):
    return 'CharField'

  def has_default(self):
    return self.default

class TestRelationshipModel():
  relationships = []
  class objects:
    def relationships(mode=None):
      return TestRelationshipModel.relationships

class RelationshipsCreateSchemaTestCase(TestCase):
  def setUp(self):
    self.non_nullable_name = 'non_nullable_name'
    self.nullable_name = 'nullable_name'
    self.one_to_one_name = 'one_to_one_name'
    self.one_to_many_name = 'one_to_many_name'
    self.many_to_many_name = 'many_to_many_name'
    self.many_to_one_name = 'many_to_one_name'
    self.non_editable_name = 'non_editable_name'
    self.default = 'default'
    TestRelationshipModel.relationships = [
      TestRelationship(name=self.non_nullable_name),
      TestRelationship(name=self.nullable_name, null=True),
      TestRelationship(name=self.one_to_one_name, one_to_one=True),
      TestRelationship(name=self.one_to_many_name, one_to_many=True),
      TestRelationship(name=self.many_to_many_name, many_to_many=True),
      TestRelationship(name=self.many_to_one_name, many_to_one=True),
      TestRelationship(name=self.non_editable_name, editable=False),
    ]

    self.schema = RelationshipsCreateSchema(TestRelationshipModel)

  def test_exclusions(self):
    print(self.schema.children.keys())
    self.assertEqual(self.schema.children.keys(), {
      self.non_nullable_name,
      self.nullable_name,
      self.one_to_one_name,
      self.one_to_many_name,
      self.many_to_many_name,
      self.many_to_one_name,
    })
    self.assertEqual(self.schema.non_nullable, {
      self.non_nullable_name,
      self.one_to_one_name,
      self.many_to_one_name,
    })

  def test_types(self):
    one_to_one_schema = self.schema.children.get(self.one_to_one_name)
    self.assertEqual(one_to_one_schema.types[0], types.UUID())

    one_to_many_schema = self.schema.children.get(self.one_to_many_name)
    self.assertEqual(one_to_many_schema.types[0], types.ARRAY())

    many_to_many_schema = self.schema.children.get(self.many_to_many_name)
    self.assertEqual(many_to_many_schema.types[0], types.ARRAY())

    many_to_one_schema = self.schema.children.get(self.many_to_one_name)
    self.assertEqual(many_to_one_schema.types[0], types.UUID())

class CreateSchemaTestCase(TestCase):
  def setUp(self):
    self.temp_id = uuid.uuid4().hex
    self.name = 'name'
    self.mock_parent = MockParentModel.objects.create(name='mock_parent')
    self.schema = CreateSchema(MockModel)

  def test_create(self):
    payload = {
      self.temp_id: {
        schema_constants.ATTRIBUTES: {
          mock_model_fields.NAME: self.name,
        },
        schema_constants.RELATIONSHIPS: {
          mock_model_fields.PARENT_NON_NULLABLE: self.mock_parent._id,
        },
      },
    }

    response = self.schema.respond(payload=payload)

    mock_model = MockModel.objects.get()
    self.assertTrue(mock_model)
    self.assertEqual(response.render(), {
      self.temp_id: mock_model._id,
    })
