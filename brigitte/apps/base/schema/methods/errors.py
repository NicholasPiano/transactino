
from util.api import Error

class QueryKeyValueNotPresentError(Error):
  code = 'bd305cb76f854a618de799fbba1c994f'
  name = 'query_key_value_not_present'
  description = 'Both key and value must be present'

class QueryAndOrPresentWithKeyValueError(Error):
  code = '660b412116bb4975a1fccfbef6cec276'
  name = 'query_and_or_present_with_key_value'
  description = 'AND and OR keys must not be present with key or value keys'

class QueryAndOrPresentError(Error):
  code = '146b16d874174273bd73e306493b34f5'
  name = 'query_and_or_present'
  description = 'A query cannot contain both AND and OR keys'

class InvalidQueryDirectiveError(Error):
  code = '4aea11e69a0847bab55483d95b5928a1'
  name = 'invalid_query_directive'
  description = 'Unrecognised directive'
  description_with_arguments = 'Invalid directive given for field [{}.{}]: [{}]'

  def __init__(self, model=None, field=None, directive=None):
    self.description = (
      self.description_with_arguments.format(model, field, directive)
      if model is not None and field is not None and directive is not None
      else self.description
    )

class filter_errors:
  QUERY_KEY_VALUE_NOT_PRESENT = QueryKeyValueNotPresentError
  QUERY_AND_OR_PRESENT_WITH_KEY_VALUE = QueryAndOrPresentWithKeyValueError
  QUERY_AND_OR_PRESENT = QueryAndOrPresentError
  INVALID_QUERY_DIRECTIVE = InvalidQueryDirectiveError

class NonNullableNotIncludedError(Error):
  code = 'a20531d1bbac4412ba026599b34ce617'
  name = 'non_nullable_not_included'
  description = 'All non-nullable fields must be included'
  description_with_arguments = 'Non-nullable fields [{}] must be included'

  def __init__(self, not_included=None):
    sorted_not_included = list(not_included).sort() if not_included is not None else None
    self.description = (
      self.description_with_arguments.format(','.join(sorted_not_included))
      if sorted_not_included is not None
      else self.description
    )

class MustContainAllNonNullableKeysError(Error):
  code = '209dd1efbb1445b6bcc6a80c455ce79c'
  name = 'must_contain_non_nullable'
  description = 'All keys with non-nullable fields must be included'
  description_with_arguments = 'Keys with non-nullable fields [{}] must be included'

  def __init__(self, must_contain=None):
    sorted_must_contain = list(must_contain).sort() if must_contain is not None else None
    self.description = (
      self.description_with_arguments.format(','.join(sorted_must_contain))
      if sorted_must_contain is not None
      else self.description
    )

class create_errors:
  NON_NULLABLE_NOT_INCLUDED = NonNullableNotIncludedError
  MUST_CONTAIN_ALL_NON_NULLABLE = MustContainAllNonNullableKeysError

class NullableMustContainKeyError(Error):
  code = 'b557465fbf7e46a4b0bc6877922ccdec'
  name = 'model_nullable_must_contain_key'
  description = 'Nullable field command must contain null key'
  description_with_arguments = 'Nullable for field [{}] must contain null key'

  def __init__(self, field=None):
    self.description = (
      self.description_with_arguments.format(field)
      if field is not None
      else self.description
    )

class NullableMustBeTrueError(Error):
  code = 'fad441c0fd3f466d90aac0623fcbfb7e'
  name = 'model_nullable_must_be_true'
  description = 'Nullable field must be true'
  description_with_arguments = 'Nullable for field [{}] must be true'

  def __init__(self, field=None):
    self.description = (
      self.description_with_arguments.format(field)
      if field is not None
      else self.description
    )

class set_errors:
  NULLABLE_MUST_CONTAIN_KEY = NullableMustContainKeyError
  NULLABLE_MUST_BE_TRUE = NullableMustBeTrueError

class DoesNotExistError(Error):
  code = '71a90b01d0c24f79bc5a56678ba8a9e9'
  name = 'does_not_exist'
  description = 'Resource does not exist'
  description_with_arguments = 'Resource with id [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class method_errors:
  DOES_NOT_EXIST = DoesNotExistError
