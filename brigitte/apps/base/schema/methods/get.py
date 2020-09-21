
from util.api import (
  Schema, ArraySchema, TemplateSchema, IndexedSchema,
  Response, ArrayResponse, IndexedResponse,
  types,
)

from .errors import method_errors
from .base import ResponseWithInternalQuerySet

class GetClientResponse(IndexedResponse, ResponseWithInternalQuerySet):
  pass

class GetClientSchema(IndexedSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=GetClientResponse,
      template=TemplateSchema(types=types.BOOLEAN()),
    )

class PrototypeResponse(Response):
  def __init__(self, *args):
    super().__init__(*args)
    self.gotten = False

  def set_gotten(self, gotten):
    self.gotten = gotten

class PrototypeSchema(Schema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=PrototypeResponse,
      types=types.UUID(),
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    instance = self.model.objects.get(id=payload)

    if instance is None:
      self.active_response.add_error(method_errors.DOES_NOT_EXIST(id=payload))
      return

    self.active_response.set_gotten(True)

class GetSchema(ArraySchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      template=PrototypeSchema(Model),
      client=GetClientSchema(),
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    gotten = {
      child_response.render(): child_response.gotten
      for child_response
      in self.active_response.children
    }

    full_queryset = self.model.objects.filter(id__in=gotten.keys())

    if full_queryset:
      self.active_response = self.client.respond(gotten)
      self.active_response.add_internal_queryset(full_queryset)
