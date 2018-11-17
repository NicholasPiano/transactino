
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.constants import model_fields
from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import ResponseWithInternalQuerySet

from ....constants import payment_fields

class PaymentGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class PaymentGetSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=PaymentGetResponse,
      children={
        model_fields.ID: Schema(types=types.UUID()),
        payment_fields.IS_OPEN: Schema(types=types.BOOLEAN()),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    id = self.active_response.force_get_child(model_fields.ID).render()

    queryset = []
    if id is not None:
      queryset = context.get_account().payments.filter(id=id)
    else:
      is_open = self.active_response.force_get_child(payment_fields.IS_OPEN).render()
      
      if is_open is None:
        queryset = context.get_account().payments.all()
      else:
        queryset = context.get_account().payments.filter(is_open=is_open)

    self.active_response.add_internal_queryset(queryset)
