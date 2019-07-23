
import json
from django.test import TestCase

from util.merge import merge
from ..types import types
from ..schema import Schema, StructureSchema, ArraySchema, IndexedSchema
from ..errors import errors
from ..constants import constants

class SchemaTestCase(TestCase):
  def setUp(self):
    self.schema = Schema(description='Some description')

  def test_simple_response(self):
    payload = 'Sample value'
    response = self.schema.respond(payload=payload)
    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = {}
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(payload=payload, types=self.schema.types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_empty(self):
    response = self.schema.respond()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.TYPES: {
        type.code: type.render()
        for type in self.schema.types
      },
      constants.ERRORS: [
        error.code
        for error in self.schema.available_errors
      ],
    })

class AsymmetricSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = Schema(
      description='Some description',
      client=Schema(types=types.BOOLEAN()),
    )

  def test_simple_response(self):
    payload = 'Sample value'
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(payload=payload, types=self.schema.client.types)

    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = {}
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(payload=payload, types=self.schema.types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_empty(self):
    response = self.schema.respond()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.TYPES: {
        type.code: type.render()
        for type in self.schema.types
      },
      constants.ERRORS: [
        error.code
        for error in self.schema.available_errors
      ],
      constants.CLIENT: self.schema.client.respond().render(),
    })

class StructureSchemaTestCase(TestCase):
  def setUp(self):
    self.test_key = 'test'
    self.description = 'Some description'
    self.schema = StructureSchema(
      description=self.description,
      children={
        self.test_key: Schema(),
      }
    )

  def test_simple_response(self):
    payload = {
      self.test_key: 'value',
    }
    response = self.schema.respond(payload=payload)
    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = 'Some string'
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(payload=payload, types=self.schema.types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_child_fails_type_validation(self):
    payload = {
      self.test_key: True,
    }
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(
      payload=payload.get(self.test_key),
      types=self.schema.children.get(self.test_key).types,
    )

    self.assertEqual(response.render(), {
      self.test_key: {
        constants.ERRORS: {
          error.code: error.render(),
        },
      },
    })

  def test_empty(self):
    self.maxDiff = None
    response = self.schema.respond()

    print(json.dumps(response.render(), indent=2))

    expected = {
      constants.DESCRIPTION: self.schema.description,
      constants.TYPES: {
        type.code: type.render()
        for type in self.schema.types
      },
      constants.ERRORS: {
        error.code: error.render()
        for error in set.union(
          self.schema.available_errors,
          self.schema.children.get(self.test_key).available_errors,
        )
      },
      constants.CHILDREN: {
        self.test_key: {
          constants.DESCRIPTION: self.schema.children.get(self.test_key).description,
          constants.TYPES: {
            type.code: type.render()
            for type in self.schema.children.get(self.test_key).types
          },
          constants.ERRORS: [
            error.code
            for error in self.schema.children.get(self.test_key).available_errors
          ],
        },
      },
    }

    print(json.dumps(expected, indent=2))

    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.TYPES: {
        type.code: type.render()
        for type in self.schema.types
      },
      constants.ERRORS: {
        error.code: error.render()
        for error in self.schema.available_errors
      },
      constants.CHILDREN: {
        self.test_key: {
          constants.DESCRIPTION: self.schema.children.get(self.test_key).description,
          constants.TYPES: {
            type.code: type.render()
            for type in self.schema.children.get(self.test_key).types
          },
          constants.ERRORS: [
            error.code
            for error in self.schema.children.get(self.test_key).available_errors
          ],
        },
      },
    })

class ArraySchemaTestCase(TestCase):
  def setUp(self):
    self.test_key = 'test'
    self.description = 'Some description'
    self.schema = ArraySchema(
      description=self.description,
      template=Schema(),
    )

  def test_simple_response(self):
    payload = [
      'value',
    ]
    response = self.schema.respond(payload=payload)
    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = 'Some string'
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(payload=payload, types=self.schema.types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_child_fails_type_validation(self):
    payload = [
      True,
    ]
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(payload=payload[0], types=self.schema.template.types)

    self.assertEqual(response.render(), [
      {
        constants.ERRORS: {
          error.code: error.render(),
        },
      },
    ])

  def test_empty(self):
    response = self.schema.respond()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.ERRORS: [
        error.code
        for error in self.schema.available_errors
      ],
      constants.TYPES: {
        type.code: type.render()
        for type in self.schema.types
      },
      constants.TEMPLATE: self.schema.template.respond().render(),
    })

class IndexedSchemaTestCase(TestCase):
  def setUp(self):
    self.test_index = 'test'
    self.description = 'Some description'
    self.schema = IndexedSchema(
      description=self.description,
      index_type=types.STRING(),
    )

  def test_simple_response(self):
    payload = {
      self.test_index: 'Some value',
    }
    response = self.schema.respond(payload=payload)
    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = 'Some string'
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(payload=payload, types=self.schema.types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_fails_type_validation_index(self):
    invalid_index = 0
    payload = {
      invalid_index: 'Some value',
    }
    response = self.schema.respond(payload=payload)

    error = errors.INVALID_INDEXES([invalid_index], self.schema.index_type)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_child_fails_type_validation(self):
    payload = {
      self.test_index: True,
    }
    response = self.schema.respond(payload=payload)

    error = errors.TYPES(
      payload=payload.get(self.test_index),
      types=self.schema.template.types,
    )

    self.assertEqual(response.render(), {
      self.test_index: {
        constants.ERRORS: {
          error.code: error.render(),
        },
      },
    })

  def test_empty(self):
    response = self.schema.respond()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.TYPES: {
        type.code: type.render()
        for type in self.schema.types
      },
      constants.TEMPLATE: self.schema.template.respond().render(),
      constants.ERRORS: {
        error.code: error.render()
        for error in set.union(
          self.schema.available_errors,
          self.schema.template.available_errors,
        )
      },
    })
