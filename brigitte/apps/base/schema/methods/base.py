
from util.api import Response

class ResponseWithInternalQuerySet(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.internal_queryset = None

  def add_internal_queryset(self, queryset):
    self.internal_queryset = queryset

class ExternalQueryset():
  def __init__(self, queryset, model=None):
    self.queryset = queryset

    if hasattr(queryset, 'model'):
      self.model = queryset.model
    else:
      self.model = model

  def __iter__(self):
    return iter(self.queryset)

class ResponseWithExternalQuerySets(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.external_querysets = []

  def add_external_queryset(self, queryset, model=None):
    if queryset is not None:
      self.external_querysets.append(ExternalQueryset(queryset, model=model))

base_client_response_classes = (
  ResponseWithInternalQuerySet,
  ResponseWithExternalQuerySets,
)
class BaseClientResponse(*base_client_response_classes):
  pass
