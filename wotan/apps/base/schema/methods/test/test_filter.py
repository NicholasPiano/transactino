
import json

from django.db.models import Q
from django.test import TestCase

from util.api import constants

from apps.base.models import MockModel, MockParentModel

from ..constants import filter_constants
from ..errors import filter_errors
from ..filter import FilterSchema

class FilterSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent_model = MockParentModel.objects.create(name='name')
    self.mock_model = MockModel.objects.create(parent_non_nullable=self.mock_parent_model, name='name')
    self.schema = FilterSchema(MockModel)

  def test_query(self):
    key1 = 'name__contains'
    value1 = 'a'

    key2 = 'parent_non_nullable__name__contains'
    value2 = 'a'

    query = Q(**{key1: value1}) | Q(**{key2: value2})

    payload = {
      filter_constants.COMPOSITE: [
        {
          filter_constants.KEY: key1,
          filter_constants.VALUE: value1,
        },
        {
          filter_constants.KEY: key2,
          filter_constants.VALUE: value2,
        },
      ],
    }

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.render(), {
      filter_constants.COUNT: 1,
      filter_constants.QUERY: str(query),
    })

  def test_query_with_both_and_and_or(self):
    payload = {
      filter_constants.COMPOSITE: [
        {
          filter_constants.AND: [],
          filter_constants.OR: [],
        },
      ],
    }

    response = self.schema.respond(payload=payload)

    query_and_or_present = filter_errors.QUERY_AND_OR_PRESENT()
    self.assertEqual(response.render(), {
      filter_constants.COMPOSITE: [
        {
          constants.ERRORS: {
            query_and_or_present.code: query_and_or_present.render(),
          },
        },
      ],
    })

  def test_query_without_key_value(self):
    key = 'name__contains'
    payload = {
      filter_constants.COMPOSITE: [
        {
          filter_constants.KEY: key,
        },
      ],
    }

    response = self.schema.respond(payload=payload)

    query_key_value_not_present = filter_errors.QUERY_KEY_VALUE_NOT_PRESENT()
    self.assertEqual(response.render(), {
      filter_constants.COMPOSITE: [
        {
          constants.ERRORS: {
            query_key_value_not_present.code: query_key_value_not_present.render(),
          },
        },
      ],
    })

  def test_query_with_key_value_and_or(self):
    key = 'name__contains'
    payload = {
      filter_constants.COMPOSITE: [
        {
          filter_constants.KEY: key,
          filter_constants.VALUE: 'value',
          filter_constants.AND: [],
        },
      ],
    }

    response = self.schema.respond(payload=payload)

    query_and_or_present_with_key_value = filter_errors.QUERY_AND_OR_PRESENT_WITH_KEY_VALUE()
    self.assertEqual(response.render(), {
      filter_constants.COMPOSITE: [
        {
          constants.ERRORS: {
            query_and_or_present_with_key_value.code: query_and_or_present_with_key_value.render(),
          },
        },
      ],
    })

  def test_query_invalid_directive(self):
    field = 'name'
    invalid_directive = 'invalid_directive'
    field_with_invalid_directive = '{}__{}'.format(field, invalid_directive)
    payload = {
      filter_constants.COMPOSITE: [
        {
          filter_constants.KEY: field_with_invalid_directive,
          filter_constants.VALUE: 'value',
        },
      ],
    }

    response = self.schema.respond(payload=payload)

    invalid_query_directive = filter_errors.INVALID_QUERY_DIRECTIVE(
      model=MockModel.__name__,
      field=field,
      directive=invalid_directive,
    )
    self.assertEqual(response.render(), {
      filter_constants.COMPOSITE: [
        {
          constants.ERRORS: {
            invalid_query_directive.code: invalid_query_directive.render(),
          },
        },
      ],
    })
