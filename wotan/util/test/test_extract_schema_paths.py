
from django.test import TestCase
from ..extract_schema_paths import extract_schema_paths

class ExtractSchemaPathsTestCase(TestCase):
  def setUp(self):
    self.key1 = 'key1'
    self.key2 = 'key2'
    self.sub1 = 'sub1'
    self.sub2 = 'sub2'
    children = '_children'
    value = 'value'
    self.schema = {
      children: {
        self.key1: {
          children: {
            self.sub1: value,
            self.sub2: value,
          },
        },
        self.key2: value,
      },
    }
    self.non_null_schema = {
      self.key1: {
        self.sub1: value,
        self.sub2: value,
      },
      self.key2: value,
    }
    self.paths = [
      [self.key1, self.sub1],
      [self.key1, self.sub2],
      [self.key2],
    ]

  def test_extract_schema_paths(self):
    self.assertEqual(extract_schema_paths(self.schema), self.paths)

  def test_extract_schema_paths_not_null(self):
    self.assertEqual(extract_schema_paths(self.non_null_schema, null=False), self.paths)
