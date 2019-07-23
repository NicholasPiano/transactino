
from django.test import TestCase

from ..types import types
from ..constants import constants
from ..errors import errors
from ..schema import (
  Schema,
  StructureSchema,
  ArraySchema,
  IndexedSchema,
)
from ..response import (
  Response,
  StructureResponse,
  ArrayResponse,
  IndexedResponse,
)

class ResponseErrorsTestCase(TestCase):
  def setUp(self):
    self.schema = Schema()

  def test_blank_has_errors(self):
    response = Response(parent_schema=self.schema)
    self.assertFalse(response.has_child_errors)
    self.assertFalse(response.has_errors())

  def test_has_errors(self):
    response = Response(parent_schema=self.schema)
    response.add_error(errors.TYPES())
    self.assertFalse(response.has_child_errors)
    self.assertTrue(response.has_errors())

class ResponseRenderTestCase(TestCase):
  def setUp(self):
    self.schema = Schema()

  def test_default_render_behaviour(self):
    response = Response(parent_schema=self.schema)
    self.assertEqual(response.render(), None)

  def test_empty_render_behaviour(self):
    response = Response(parent_schema=self.schema)
    response.is_empty = True
    error = errors.TYPES()
    type = types.STRING()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: response.description,
      constants.TYPES: {
        type.code: type.render(),
      },
      constants.ERRORS: [
        error.code
      ],
    })

  def test_empty_render_behaviour_with_client_schema(self):
    response = Response(parent_schema=self.schema)
    response.client_schema = Schema()
    response.is_empty = True
    error = errors.TYPES()
    type = types.STRING()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: response.description,
      constants.TYPES: {
        type.code: type.render(),
      },
      constants.ERRORS: [
        error.code,
      ],
      constants.CLIENT: {
        constants.DESCRIPTION: response.client_schema.description,
        constants.TYPES: {
          type.code: type.render(),
        },
        constants.ERRORS: [
          error.code,
        ],
      },
    })

  def test_render_behaviour_with_errors(self):
    response = Response(parent_schema=self.schema)
    error = errors.TYPES()
    response.add_error(error)
    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_render_behaviour_with_value(self):
    response = Response(parent_schema=self.schema)
    value = 'some value'
    response.add_value(value)
    self.assertEqual(response.render(), value)

class StructureResponseChildrenTestCase(TestCase):
  child_key = 'child_key'

  def setUp(self):
    self.schema = StructureSchema(
      children={
        self.child_key: Schema(),
      },
    )

  def test_add_child(self):
    response = StructureResponse(parent_schema=self.schema)
    child_response = Response(parent_schema=self.schema.children.get(self.child_key))
    response.add_child(self.child_key, child_response)
    self.assertTrue(self.child_key in response.children)

  def test_get_child(self):
    response = StructureResponse(parent_schema=self.schema)

    self.assertIsNone(response.get_child(self.child_key))

    child_response = Response(parent_schema=self.schema.children.get(self.child_key))
    response.add_child(self.child_key, child_response)

    self.assertEquals(response.get_child(self.child_key), child_response)

  def test_get_missing_child(self):
    response = StructureResponse(parent_schema=self.schema)

    self.assertIsNone(response.get_child(self.child_key))

    child_response = Response(parent_schema=self.schema.children.get(self.child_key))

    self.assertEquals(response.force_get_child(self.child_key).parent_schema, child_response.parent_schema)

  def test_get_nonexistant_child(self):
    response = StructureResponse(parent_schema=self.schema)
    child_response = Response(parent_schema=self.schema.children.get(self.child_key))
    response.add_child(self.child_key, child_response)

    self.assertIsNone(response.get_child('other_child_key'))
    self.assertIsNone(response.force_get_child('other_child_key'))

class StructureResponseRenderTestCase(TestCase):
  child_key = 'child_key'

  def setUp(self):
    self.schema = StructureSchema(
      children={
        self.child_key: Schema(),
      },
    )

  def test_empty_render_behaviour(self):
    response = StructureResponse(parent_schema=self.schema)
    response.is_empty = True

    child_response = Response(parent_schema=self.schema.children.get(self.child_key))
    child_response.is_empty = True

    response.add_child(self.child_key, child_response)

    errors = self.schema.available_errors
    types = self.schema.types

    self.assertEqual(response.render(), {
      constants.DESCRIPTION: response.description,
      constants.TYPES: {
        type.code: type.render()
        for type in types
      },
      constants.ERRORS: {
        error.code: error.render()
        for error in errors
      },
      constants.CHILDREN: {
        self.child_key: child_response.render(),
      }
    })
