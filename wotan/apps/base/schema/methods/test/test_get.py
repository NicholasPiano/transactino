
import uuid

from django.db import models
from django.test import TestCase

from util.api import constants

from apps.base.models import MockParentModel

from ..errors import method_errors
from ..get import GetSchema

class GetSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent = MockParentModel.objects.create(name='mock_parent')
    self.schema = GetSchema(MockParentModel)

  def test_get(self):
    payload = [
      self.mock_parent._id,
    ]

    response = self.schema.respond(payload=payload)

    self.assertEqual(response.render(), {
      self.mock_parent._id: True,
    })

  def test_get_with_does_not_exist(self):
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
