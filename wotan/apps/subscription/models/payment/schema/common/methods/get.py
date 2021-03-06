
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
from .errors import get_errors

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

    payment_id = self.get_child_value(get_constants.PAYMENT_ID)

    queryset = []
    if payment_id is not None:
      queryset = context.get_account().payments.filter(id=payment_id)

      if not queryset:
        self.active_response.add_error(
          get_errors.PAYMENT_DOES_NOT_EXIST(id=payment_id)
        )
        return

    else:
      is_open = self.get_child_value(payment_fields.IS_OPEN)

      if is_open is None:
        queryset = context.get_account().payments.all()
      else:
        queryset = context.get_account().payments.filter(is_open=is_open)

    self.active_response.add_internal_queryset(queryset)
