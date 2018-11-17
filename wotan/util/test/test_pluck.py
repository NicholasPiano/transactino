
from django.test import TestCase
from util.pluck import pluck

class keys:
  key1 = 'key1'
  key2 = 'key2'

class values:
  value1 = 'value1'
  value2 = 'value2'

class PluckTestCase(TestCase):
  def setUp(self):
    self.dictionary = {
      keys.key1: values.value1,
      keys.key2: values.value2,
    }

  def test_pluck(self):
    self.assertEqual(list(pluck(self.dictionary, keys.key1, keys.key2)), [values.value1, values.value2])
