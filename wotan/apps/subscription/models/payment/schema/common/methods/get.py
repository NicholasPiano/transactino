
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
from .constants import get_constants

class PaymentGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class PaymentGetSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Payment get method.'
        ' It can be filtered by the open status of'
        ' the payment and the payment ID'
      ),
      response=PaymentGetResponse,
      children={
        get_constants.PAYMENT_ID: Schema(
          description='The payment ID',
          types=types.UUID(),
        ),
        payment_fields.IS_OPEN: Schema(
          description='The payment open status',
          types=types.BOOLEAN(),
        ),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    id = self.active_response.force_get_child(get_constants.PAYMENT_ID).render()

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
