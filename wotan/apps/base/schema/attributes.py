
from util.force_array import force_array
from util.api import Schema, StructureSchema, StructureResponse, types

from .errors import model_schema_errors

class AttributeResponse(StructureResponse):
  def __init__(self, parent_schema):
    self.is_inclusive = False
    self.should_include_attributes = True
    super().__init__(parent_schema)

  def get_attributes(self):
    attribute_names = {
      field.name
      for field in self.parent_schema.model.objects.attributes(
        mode=self.parent_schema.mode,
      )
    }
    child_keys = self.children.keys()

    if not self.should_include_attributes:
      return []

    if not child_keys:
      return list(attribute_names)

    if self.is_inclusive:
      return list(child_keys)

    return list(attribute_names - child_keys)

class AttributeSchema(StructureSchema):
  default_types = force_array(StructureSchema.default_types) + [
    types.BOOLEAN(),
  ]

  def __init__(self, Model, mode=None, **kwargs):
    self.model = Model
    self.mode = mode
    super().__init__(
      **kwargs,
      response=AttributeResponse,
      children={
        attribute.name: Schema(
          description='',
          types=types.BOOLEAN(),
        )
        for attribute in Model.objects.attributes(mode=mode)
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        model_schema_errors.UNIFORM_INCLUSIVE(),
      },
    )

  def passes_pre_response_checks(self, payload):
    if self.active_response.active_type == types.BOOLEAN():
      return True

    values = payload.values()
    if any(values) and not all(values):
      self.active_response.add_error(model_schema_errors.UNIFORM_INCLUSIVE())
      return False

    if all(values):
      self.active_response.is_inclusive = True

    return super().passes_pre_response_checks(payload)

  def responds_to_valid_payload(self, payload, context):
    if self.active_response.active_type == types.BOOLEAN():
      self.active_response.should_include_attributes = payload
      return

    super().responds_to_valid_payload(payload, context)
