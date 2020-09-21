
APP_LABEL = 'base'

query_directive_array = [
  'startswith',
  'contains',
  'icontains',
]

class query_directives:
  JOIN = '__'

for directive in query_directive_array:
  setattr(query_directives, directive.upper(), directive)

def is_valid_query_directive(directive):
  return directive in query_directive_array

class model_fields:
  ID = 'id'
  DATE_CREATED = 'date_created'

class mock_model_constants:
  PARENT_RELATED_MODEL = 'base.MockParentModel'
  PARENT_RELATED_NAME = 'children'
  PARENT_NON_NULLABLE_RELATED_MODEL = 'base.MockParentModel'
  PARENT_NON_NULLABLE_RELATED_NAME = 'children_nn'
  UNDER_RELATED_MODEL = 'base.MockModel'
  UNDER_RELATED_NAME = 'over'

class mock_model_fields:
  NAME = 'name'
  PARENT = 'parent'
  PARENT_NON_NULLABLE = 'parent_non_nullable'
  UNDER = 'under'
