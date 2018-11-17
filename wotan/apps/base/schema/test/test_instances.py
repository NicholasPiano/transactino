
import json
from django.db import models
from django.test import TestCase

from util.api import errors, constants

from ...models import MockParentModel, MockModel
from ..constants import schema_constants
from ..instances import InstancesClosedSchema, InstancesResponse

class InstancesSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent_model = MockParentModel.objects.create(name='name')
    self.mock_model = MockModel.objects.create(parent_non_nullable=self.mock_parent_model, name='name')
    self.schema = InstancesClosedSchema(MockModel)

  def test_closed_schema(self):
    payload = {
      'aacf56cf7869476786531d575a4afab7': {
        'attributes': None,
      },
    }

    response = self.schema.respond(payload=payload)
    error = errors.CLOSED()

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

class InstancesResponseTestCase(TestCase):
  def setUp(self):
    self.schema = InstancesClosedSchema(MockModel)
    self.response = self.schema.get_response()

  def test_add_instances(self):
    mock_parent_model = MockParentModel.objects.create(name='parent')
    instances = [
      MockModel.objects.create(name='name1', parent_non_nullable=mock_parent_model),
      MockModel.objects.create(name='name2', parent_non_nullable=mock_parent_model),
      MockModel.objects.create(name='name3', parent_non_nullable=mock_parent_model),
    ]
    attributes = ['name']
    relationships = ['parent_non_nullable']

    self.response.add_attributes(attributes)
    self.response.add_relationships(relationships)
    self.response.add_instances(instances)

    self.assertEqual(self.response.render(), {
      instance._id: {
        schema_constants.ATTRIBUTES: {
          attributes[0]: getattr(instance, attributes[0]),
        },
        schema_constants.RELATIONSHIPS: {
          relationships[0]: getattr(instance, relationships[0])._ref,
        }
      }
      for instance in instances
    })
