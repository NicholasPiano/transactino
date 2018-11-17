
from util.api import Error

class QueryKeyValueNotPresentError(Error):
  code = '008'
  name = 'query_key_value_not_present'
  description = 'Both key and value must be present'

class QueryAndOrPresentWithKeyValueError(Error):
  code = '009'
  name = 'query_and_or_present_with_key_value'
  description = 'AND and OR keys must not be present with key or value keys'

class QueryAndOrPresentError(Error):
  code = '010'
  name = 'query_and_or_present'
  description = 'A query cannot contain both AND and OR keys'

class InvalidQueryDirectiveError(Error):
  code = '013'
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
  code = '006'
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
  code = '007'
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
  code = '014'
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
  code = '015'
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
  code = '017'
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
