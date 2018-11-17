
from django.test import TestCase
from util.force_array import force_array

class ForceArrayTestCase(TestCase):
  def setUp(self):
    self.array_like = ['lm1', 'lm2']
    self.non_array_like = 'value'

  def test_force_array_array_like(self):
    self.assertEqual(force_array(self.array_like), self.array_like)

  def test_force_array_non_array_like(self):
    self.assertEqual(force_array(self.non_array_like), [self.non_array_like])
