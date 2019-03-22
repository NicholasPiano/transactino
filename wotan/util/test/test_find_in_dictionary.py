
from django.test import TestCase
from ..find_in_dictionary import find_in_dictionary

class FindInDictionaryTestCase(TestCase):
  def setUp(self):
    pass

  def test_not_a_dictionary(self):
    self.assertFalse(find_in_dictionary([], []))

  def test_no_path_list(self):
    self.assertEqual(find_in_dictionary({}, []), {})

  def test_first_path_no_match(self):
    path = 'path'
    dictionary = {
      'other_path': 'value'
    }

    self.assertFalse(find_in_dictionary(dictionary, [path]))

  def test_correct_path(self):
    first_path = 'first_path'
    value = 'value'

    dictionary = {
      first_path: value,
    }

    self.assertEqual(
      find_in_dictionary(
        dictionary,
        [
          first_path,
        ],
      ),
      value,
    )

  def test_with_rest(self):
    first_path = 'first_path'
    second_path = 'second_path'
    value = 'value'

    dictionary = {
      first_path: {
        second_path: value,
      },
    }

    self.assertEqual(
      find_in_dictionary(
        dictionary,
        [
          first_path,
          second_path,
        ],
      ),
      value,
    )
