
from util.api import Response

class ResponseWithInternalQuerySet(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.internal_queryset = None

  def add_internal_queryset(self, queryset):
    self.internal_queryset = queryset

class ResponseWithExternalQuerySets(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.external_querysets = []

  def add_external_queryset(self, queryset):
    if queryset is not None:
      self.external_querysets.append(queryset)

base_client_response_classes = (
  ResponseWithInternalQuerySet,
  ResponseWithExternalQuerySets,
)
class BaseClientResponse(*base_client_response_classes):
  pass
