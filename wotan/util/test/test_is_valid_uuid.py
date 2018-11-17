
import uuid

from django.test import TestCase
from util.is_valid_uuid import is_valid_uuid

class IsValidUUIDTestCase(TestCase):
  def setUp(self):
    self.valid_uuid = uuid.uuid4()
    self.other_valid_uuid = str(uuid.uuid4())
    self.invalid_uuid = 'some value'

  def test_valid_uuid(self):
    self.assertTrue(is_valid_uuid(self.valid_uuid))
    self.assertTrue(is_valid_uuid(self.other_valid_uuid))

  def test_invalid_uuid(self):
    self.assertFalse(is_valid_uuid(self.invalid_uuid))
