
from django.test import TestCase
from util.merge import merge

class keys:
  integer = 'integer'
  string = 'string'
  string2 = 'string2'
  list = 'list'
  dictionary = 'dictionary'
  nested = 'nested'
  nested2 = 'nested2'
  nested3 = 'nested3'
  some_key = 'some key'

class values:
  integer = 5
  integer2 = 16
  integer3 = 18
  some_string = 'some string'
  some_string2 = 'some string2'
  some_other_string = 'some other string'
  some_other_string2 = 'some other string2'
  lm1 = 'lm1'
  lm2 = 'lm2'
  lm3 = 'lm3'
  lm4 = 'lm4'
  lm5 = 'lm5'
  lm6 = 'lm6'
  lm7 = 'lm7'
  some_nested_string = 'some nested string'
  something = 'something'
  nested_lm1 = 'nested lm1'
  changed_nested_string = 'changed nested string'
  some_other_nested_string = 'some other nested string'
  other_nested_lm1 = 'other nested lm1'
  this_list_is_now_a_string = 'this list is now a string'
  this_dictionary_is_now_a_string = 'this dictionary is now a string'

class MergeTestCase(TestCase):
  def setUp(self):
    self.dictionary_one = {
      keys.integer: values.integer,
      keys.string: values.some_string,
      keys.string2: values.some_string2,
      keys.list: [values.lm1, values.lm2, values.lm3],
      keys.dictionary: {
        keys.nested: {
          keys.string: values.some_nested_string,
          keys.list: [values.nested_lm1],
        },
        keys.nested2: {
          keys.some_key: values.something,
        }
      },
    }
    self.dictionary_two = {
      keys.integer: values.integer2,
      keys.string: values.some_other_string,
      keys.list: [values.lm4, values.lm5, values.lm6],
      keys.dictionary: {
        keys.nested: {
          keys.string: values.changed_nested_string,
        },
        keys.nested3: {
          keys.string: values.some_other_nested_string,
          keys.list: [values.other_nested_lm1],
        },
      },
    }
    self.dictionary_three = {
      keys.integer: values.integer3,
      keys.string2: values.some_other_string2,
      keys.list: [values.lm7],
      keys.dictionary: {
        keys.nested: {
          keys.list: values.this_list_is_now_a_string,
        },
        keys.nested2: values.this_dictionary_is_now_a_string,
      },
    }

  def test_merge(self):
    merged_dictionary = merge(None, self.dictionary_one, self.dictionary_two, self.dictionary_three)

    self.assertEqual(merged_dictionary, {
      keys.integer: values.integer3,
      keys.string: values.some_other_string,
      keys.string2: values.some_other_string2,
      keys.list: [values.lm1, values.lm2, values.lm3, values.lm4, values.lm5, values.lm6, values.lm7],
      keys.dictionary: {
        keys.nested: {
          keys.string: values.changed_nested_string,
          keys.list: values.this_list_is_now_a_string,
        },
        keys.nested2: values.this_dictionary_is_now_a_string,
        keys.nested3: {
          keys.string: values.some_other_nested_string,
          keys.list: [values.other_nested_lm1],
        },
      },
    })
