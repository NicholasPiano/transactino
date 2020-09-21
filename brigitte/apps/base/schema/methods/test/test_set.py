
import json
import uuid

from django.db import models
from django.test import TestCase

from util.api import (
  Schema, StructureSchema,
  constants,
  types, map_type,
  errors,
)

from apps.base.constants import mock_model_fields
from apps.base.models import MockModel, MockParentModel

from ...constants import schema_constants
from ..constants import set_constants
from ..errors import set_errors, method_errors
from ..set import (
  PropertyResponse,
  NullableSchema,
  PropertiesResponse,
  AttributeSchema,
  SingleSchema,
  ManySchema,
  RelationshipManySchema,
  RelationshipSchema,
  SetSchema,
)

class PropertyResponseTestCase(TestCase):
  def setUp(self):
    self.test_key = 'test_key'
    self.schema = StructureSchema(
      children={
        self.test_key: Schema(
          types=types.UUID(),
          response=PropertyResponse,
        ),
      },
    )

  def test_should_render(self):
    payload = {
      self.test_key: uuid.uuid4().hex,
    }

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.render(), {})

  def test_should_render_with_errors(self):
    payload = {
      self.test_key: 'string',
    }

    response = self.schema.respond(payload=payload)

    type_error = errors.TYPES(
      payload=payload.get(self.test_key),
      types=self.schema.children.get(self.test_key).types,
    )
    self.assertEqual(response.render(), {
      self.test_key: {
        constants.ERRORS: {
          type_error.code: type_error.render()
        },
      },
    })

class NullableSchemaTestCase(TestCase):
  class nullable_field:
    null = True
    name = 'nullable'

  class non_nullable_field:
    null = False
    name = 'non-nullable'

  def setUp(self):
    self.schema = NullableSchema(self.nullable_field)
    self.non_nullable_schema = NullableSchema(self.non_nullable_field)

  def test_nullable(self):
    payload = {
      set_constants.NULL: True,
    }

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.get_property(), None)

  def test_nullable_no_key(self):
    payload = {}

    response = self.schema.respond(payload=payload)

    nullable_must_contain_key = set_errors.NULLABLE_MUST_CONTAIN_KEY(field=self.nullable_field.name)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        nullable_must_contain_key.code: nullable_must_contain_key.render(),
      },
    })

  def test_nullable_false(self):
    payload = {
      set_constants.NULL: False,
    }

    response = self.schema.respond(payload=payload)

    nullable_must_be_true = set_errors.NULLABLE_MUST_BE_TRUE(field=self.nullable_field.name)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        nullable_must_be_true.code: nullable_must_be_true.render(),
      },
    })

class PropertiesResponseTestCase(TestCase):
  def setUp(self):
    self.test_key = 'test_key'
    self.schema = StructureSchema(
      response=PropertiesResponse,
      children={
        self.test_key: Schema(
          types=types.UUID(),
          response=PropertyResponse,
        ),
      },
    )

  def test_get_properties(self):
    payload = {
      self.test_key: uuid.uuid4().hex,
    }

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.render(), {})
    self.assertEqual(response.get_properties(), payload)

class AttributeSchemaTestCase(TestCase):
  class attribute:
    def __init__(self, null=True, verbose_name=None):
      self.null = null
      self.verbose_name = verbose_name

    def get_internal_type(self):
      return 'CharField'

  def setUp(self):
    self.nullable_attribute = self.attribute(verbose_name='nullable_attribute')
    self.nullable_attribute_schema = AttributeSchema(self.nullable_attribute)

    self.non_nullable_attribute = self.attribute(null=False, verbose_name='non_nullable_attribute')
    self.non_nullable_attribute_schema = AttributeSchema(self.non_nullable_attribute)

  def test_nullable_types(self):
    self.assertEqual(self.nullable_attribute_schema.types, [
      map_type(self.nullable_attribute.get_internal_type()),
      types.STRUCTURE(),
    ])

  def test_non_nullable_types(self):
    self.assertEqual(self.non_nullable_attribute_schema.types, [
      map_type(self.non_nullable_attribute.get_internal_type()),
    ])

class SingleSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent1 = MockParentModel.objects.create(name='1')
    self.mock_model = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='name')
    self.mock_other1 = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='other1')

    self.schema = SingleSchema(MockModel._meta.get_field(mock_model_fields.UNDER))

  def test_valid_related_object(self):
    payload = self.mock_other1._id

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.render(), payload)

  def test_nonexistent_related_object(self):
    payload = uuid.uuid4().hex

    response = self.schema.respond(payload=payload)

    does_not_exist = method_errors.DOES_NOT_EXIST(id=payload)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        does_not_exist.code: does_not_exist.render(),
      },
    })

class ManySchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent1 = MockParentModel.objects.create(name='1')
    self.mock_model = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='name')
    self.mock_other1 = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='other1')
    self.mock_other2 = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='other2')

    self.schema = ManySchema(MockModel._meta.get_field(mock_model_fields.UNDER))

  def test_many(self):
    payload = [
      self.mock_other1._id,
      self.mock_other2._id,
    ]

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.get_property(), payload)

class RelationshipManySchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent1 = MockParentModel.objects.create(name='1')
    self.mock_model = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='name')
    self.mock_other1 = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='other1')
    self.mock_other2 = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='other2')

    self.schema = RelationshipManySchema(MockModel._meta.get_field(mock_model_fields.UNDER))

  def test_relationship_many(self):
    payload = {
      set_constants.ADD: [
        self.mock_other1._id,
      ],
      set_constants.REMOVE: [
        self.mock_other2._id,
      ],
    }

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.get_property(), payload)

class RelationshipSchemaTestCase(TestCase):
  def setUp(self):
    self.many_to_many_relationship_schema = RelationshipSchema(
      MockModel._meta.get_field(mock_model_fields.UNDER),
    )
    self.non_nullable_relationship_schema = RelationshipSchema(
      MockModel._meta.get_field(mock_model_fields.PARENT_NON_NULLABLE),
    )
    self.nullable_relationship_schema = RelationshipSchema(
      MockModel._meta.get_field(mock_model_fields.PARENT),
    )

  def test_many_to_one_relationship_schema_types(self):
    self.assertEqual(self.many_to_many_relationship_schema.types, [types.STRUCTURE()])

  def test_non_nullable_relationship_schema_types(self):
    self.assertEqual(self.non_nullable_relationship_schema.types, [types.UUID()])

  def test_nullable_relationship_schema_types(self):
    self.assertEqual(self.nullable_relationship_schema.types, [
      types.UUID(),
      types.STRUCTURE(),
    ])

  def test_response_with_does_not_exist(self):
    payload = uuid.uuid4().hex

    response = self.nullable_relationship_schema.respond(payload=payload)

    does_not_exist = method_errors.DOES_NOT_EXIST(id=payload)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        does_not_exist.code: does_not_exist.render(),
      },
    })

class SetSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent1 = MockParentModel.objects.create(name='1')
    self.mock_parent2 = MockParentModel.objects.create(name='2')
    self.name = 'name'
    self.mock_model = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name=self.name)
    self.mock_other1 = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='other1')
    self.mock_other2 = MockModel.objects.create(parent_non_nullable=self.mock_parent1, name='other2')
    self.mock_model.under.add(self.mock_other1)

    self.schema = SetSchema(MockModel)

  def test_set_name(self):
    self.assertEqual(self.mock_model.name, self.name)

    test_name = 'test_name'
    payload = {
      self.mock_model._id: {
        schema_constants.ATTRIBUTES: {
          mock_model_fields.NAME: test_name,
        },
      },
    }

    response = self.schema.respond(payload=payload)

    self.mock_model.refresh_from_db()

    self.assertEqual(self.mock_model.name, test_name)

  def test_set_nullable(self):
    self.assertEqual(self.mock_model.parent_non_nullable, self.mock_parent1)

    payload = {
      self.mock_model._id: {
        schema_constants.RELATIONSHIPS: {
          mock_model_fields.PARENT_NON_NULLABLE: self.mock_parent2._id,
        },
      },
    }

    response = self.schema.respond(payload=payload)

    self.mock_model.refresh_from_db()

    self.assertEqual(self.mock_model.parent_non_nullable, self.mock_parent2)

  def test_many_to_many(self):
    self.assertEqual(list(self.mock_model.under.all()), [self.mock_other1])

    payload = {
      self.mock_model._id: {
        schema_constants.RELATIONSHIPS: {
          mock_model_fields.UNDER: {
            set_constants.ADD: [
              self.mock_other2._id,
            ],
            set_constants.REMOVE: [
              self.mock_other1._id,
            ],
          },
        },
      },
    }

    response = self.schema.respond(payload=payload)

    self.mock_model.refresh_from_db()

    self.assertEqual(list(self.mock_model.under.all()), [self.mock_other2])
