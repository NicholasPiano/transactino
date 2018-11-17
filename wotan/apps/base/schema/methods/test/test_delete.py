
import uuid

from django.db import models
from django.test import TestCase

from util.api import constants

from apps.base.models import MockParentModel

from ..errors import method_errors
from ..delete import DeleteSchema

class DeleteSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent = MockParentModel.objects.create(name='mock_parent')
    self.schema = DeleteSchema(MockParentModel)

  def test_delete(self):
    self.assertTrue(MockParentModel.objects.get())

    payload = [
      self.mock_parent._id,
    ]

    response = self.schema.respond(payload=payload)

    self.assertFalse(MockParentModel.objects.get())

  def test_delete_does_not_exist(self):

    self.assertTrue(MockParentModel.objects.get())

    test_id = uuid.uuid4().hex
    payload = [
      test_id,
    ]

    response = self.schema.respond(payload=payload)

    does_not_exist = method_errors.DOES_NOT_EXIST(id=test_id)
    self.assertEqual(response.render(), [
      {
        constants.ERRORS: {
          does_not_exist.code: does_not_exist.render(),
        },
      },
    ])

    self.assertTrue(MockParentModel.objects.get())
