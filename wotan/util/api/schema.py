
from util.merge import merge
from util.force_array import force_array

from .response import (
  Response,
  StructureResponse,
  ArrayResponse,
  IndexedResponse,
)
from .errors import errors
from .types import types
from .constants import constants

class Schema():
  default_types = [
    types.STRING(),
  ]
  default_response = Response

  def __init__(self, description=None, types=None, response=None, client=None, closed=False):
    self.description = description
    self.types = force_array(types or self.default_types)
    self.response = response or self.default_response
    self.client = client
    self.switched_to_type_schema = False
    self.available_errors = self.get_available_errors()

  def get_available_errors(self):
    return {
      errors.TYPES(),
    }

  def get_response(self):
    return self.response(self)

  def respond(self, payload=None, context=None):
    self.active_response = self.get_response()

    if payload is None:
      self.responds_to_none(context)
      return self.active_response

    if not self.passes_type_validation(payload, context):
      return self.active_response

    if self.switched_to_type_schema:
      return self.active_response.active_type.schema.respond(payload=payload, context=context)

    if not self.passes_pre_response_checks(payload, context):
      return self.active_response

    self.responds_to_valid_payload(payload, context)

    return self.active_response

  def responds_to_none(self, context):
    self.active_response.is_empty = True

  def passes_type_validation(self, payload, context):
    for type in self.types:
      if type.validate(payload):
        if type.schema is not None:
          self.switched_to_type_schema = True
        self.active_response.active_type = type
        return True

    self.active_response.add_error(errors.TYPES(payload=payload, types=self.types))
    return False

  def passes_pre_response_checks(self, payload, context):
    return True

  def responds_to_valid_payload(self, payload, context):
    self.active_response.add_value(payload)

class ClosedSchema(Schema):
  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        errors.CLOSED(),
      },
    )

  def get_response(self):
    if self.client is not None:
      return self.client.get_response()

  def respond(self, payload=None, context=None):
    self.active_response = super().get_response()

    if payload is not None:
      self.active_response.add_error(errors.CLOSED())
      return self.active_response

    return super().respond(payload=payload, context=context)

  def responds_to_none(self, context):
    self.active_response = super().get_response()
    return super().responds_to_none(context)

class StructureSchema(Schema):
  default_types = [
    types.STRUCTURE(),
  ]
  default_response = StructureResponse

  def __init__(self, children={}, **kwargs):
    super().__init__(**kwargs)
    self.children = children

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        errors.INVALID_KEYS(),
      },
    )

  def responds_to_none(self, context):
    super().responds_to_none(context)
    for child_key, child_schema in self.children.items():
      self.active_response.add_child(child_key, child_schema.respond(context=context))

  def passes_pre_response_checks(self, payload, context):
    invalid_keys = payload.keys() - self.children.keys()
    if invalid_keys:
      for invalid_key in invalid_keys:
        self.active_response.add_error(errors.INVALID_KEYS(invalid_keys))
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    for child_key, child_schema in self.children.items():
      if child_key in payload:
        self.active_response.add_child(
          child_key,
          child_schema.respond(
            payload=payload.get(child_key),
            context=context,
          ),
        )

class ArraySchema(Schema):
  default_types = [
    types.ARRAY(),
  ]
  default_response = ArrayResponse

  def __init__(self, template=None, **kwargs):
    super().__init__(**kwargs)
    self.template = template

  def responds_to_valid_payload(self, payload, context):
    for child_payload in payload:
      self.active_response.add_child(
        self.template.respond(
          payload=child_payload,
          context=context,
        ),
      )

class TemplateSchema(Schema):
  def respond(self, key=None, payload=None, context=None):
    self.active_response = self.get_response()

    if payload is None:
      self.responds_to_none(context)
      return self.active_response

    if not self.passes_type_validation(key, payload, context):
      return self.active_response

    if self.switched_to_type_schema:
      return self.active_response.active_type.schema.respond(
        key=key,
        payload=payload,
        context=context,
      )

    if not self.passes_pre_response_checks(key, payload, context):
      return self.active_response

    self.responds_to_valid_payload(key, payload, context)

    return self.active_response

  def passes_type_validation(self, key, payload, context):
    return super().passes_type_validation(payload, context)

  def passes_pre_response_checks(self, key, payload, context):
    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, key, payload, context):
    super().responds_to_valid_payload(payload, context)

class IndexedSchema(Schema):
  default_types = [
    types.STRUCTURE(),
  ]
  default_index_type = types.UUID()
  default_response = IndexedResponse
  default_template = TemplateSchema

  def __init__(self, index_type=None, template=None, **kwargs):
    super().__init__(**kwargs)
    self.index_type = index_type or self.default_index_type
    self.template = template or self.default_template()

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        errors.INVALID_INDEXES(),
      },
    )

  def passes_type_validation(self, payload, context):
    passes_type_validation = super().passes_type_validation(payload, context)
    if not passes_type_validation:
      return False

    invalid_indexes = [
      index
      for index in payload.keys()
      if not self.index_type.validate(index)
    ]

    if invalid_indexes:
      self.active_response.add_error(
        errors.INVALID_INDEXES(
          indexes=invalid_indexes,
          index_type=self.index_type,
        ),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    for child_index, child_payload in payload.items():
      self.active_response.add_child(
        child_index,
        self.template.respond(
          key=child_index,
          payload=child_payload,
          context=context,
        ),
      )
