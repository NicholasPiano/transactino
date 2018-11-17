
from util.api import (
  Schema, ArraySchema, TemplateSchema, IndexedSchema,
  Response, ArrayResponse, IndexedResponse,
  types,
)

from .errors import method_errors

class DeleteClientSchema(IndexedSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      template=TemplateSchema(types=types.BOOLEAN()),
    )

class PrototypeResponse(Response):
  def __init__(self, *args):
    super().__init__(*args)
    self.deleted = False

  def set_deleted(self, deleted):
    self.deleted = deleted

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

    instance.delete()
    self.active_response.set_deleted(True)

class DeleteSchema(ArraySchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      template=PrototypeSchema(Model),
      client=DeleteClientSchema(),
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    deleted = {
      child_response.render(): child_response.deleted
      for child_response
      in self.active_response.children
    }

    self.active_response = self.client.respond(deleted)
