
from django.db.models import Q

from util.pluck import pluck
from util.api import (
  Schema, StructureSchema, ArraySchema, IndexedSchema,
  Response, StructureResponse, ArrayResponse,
  types,
  constants,
)

from .base import ResponseWithInternalQuerySet
from .constants import filter_constants
from .errors import filter_errors

class QueryResponse(StructureResponse):
  def get_query(self):
    if filter_constants.KEY in self.children:
      key_response = self.get_child(filter_constants.KEY)
      value_response = self.get_child(filter_constants.VALUE)

      return Q(**{key_response.render(): value_response.render()})
    else:
      [response] = self.children.values()
      return response.get_query()

class QuerySchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=QueryResponse,
      children={
        filter_constants.KEY: Schema(
          description='',
          types=types.STRING(),
        ),
        filter_constants.VALUE: Schema(
          description='',
          types=types.STRING(),
        ),
        filter_constants.AND: ArraySchema(
          template=Schema(),
        ),
        filter_constants.OR: ArraySchema(
          template=Schema(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        filter_errors.QUERY_AND_OR_PRESENT(),
        filter_errors.QUERY_KEY_VALUE_NOT_PRESENT(),
        filter_errors.QUERY_AND_OR_PRESENT_WITH_KEY_VALUE(),
        filter_errors.INVALID_QUERY_DIRECTIVE(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if filter_constants.AND in payload and filter_constants.OR in payload:
      self.active_response.add_error(filter_errors.QUERY_AND_OR_PRESENT())
      return False

    if filter_constants.KEY in payload or filter_constants.VALUE in payload:
      if filter_constants.KEY not in payload or filter_constants.VALUE not in payload:
        self.active_response.add_error(filter_errors.QUERY_KEY_VALUE_NOT_PRESENT())
        return False

      if filter_constants.AND in payload or filter_constants.OR in payload:
        self.active_response.add_error(filter_errors.QUERY_AND_OR_PRESENT_WITH_KEY_VALUE())
        return False

      key = payload.get(filter_constants.KEY)
      query_anomalies = self.model.objects.query_check(key)

      if query_anomalies:
        for model_name, field_name, directive in query_anomalies:
          self.active_response.add_error(filter_errors.INVALID_QUERY_DIRECTIVE(
            model=model_name,
            field=field_name,
            directive=directive,
          ))

        return False

    return super().passes_pre_response_checks(payload, context)

class CompositeResponse(ArrayResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.OR = parent_schema.OR

  def get_query(self):
    if self.has_errors() or not self.children:
      return None

    query = Q()
    for child in self.children:
      if self.OR:
        query = query | child.get_query()
      else:
        query = query & child.get_query()

    return query

class CompositeSchema(ArraySchema):
  def __init__(self, Model, OR=True, **kwargs):
    super().__init__(
      **kwargs,
      response=CompositeResponse,
      template=QuerySchema(Model),
    )
    self.model = Model
    self.OR = OR

  def responds_to_valid_payload(self, payload, context):
    self.template.children.update({
      filter_constants.AND: CompositeSchema(self.model, OR=False),
      filter_constants.OR: CompositeSchema(self.model),
    })
    super().responds_to_valid_payload(payload, context)

class FilterClientResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class FilterClientSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=FilterClientResponse,
      children={
        filter_constants.COUNT: Schema(types=types.INTEGER()),
        filter_constants.QUERY: Schema(),
      },
    )

class FilterSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      client=FilterClientSchema(),
      children={
        filter_constants.COMPOSITE: CompositeSchema(Model),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    composite_response = self.active_response.force_get_child(filter_constants.COMPOSITE)
    composite_query = composite_response.get_query()

    if composite_query is not None:
      full_queryset = self.model.objects.filter(composite_query)
      filter_client_payload = {
        filter_constants.COUNT: full_queryset.count(),
        filter_constants.QUERY: str(composite_query),
      }

      self.active_response = self.client.respond(payload=filter_client_payload)
      self.active_response.add_internal_queryset(full_queryset)
