
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.constants import model_fields
from apps.base.schema.methods.base import ResponseWithInternalQuerySet

from ....constants import transaction_report_fields

class TransactionReportGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class TransactionReportGetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the TransactionReport get method.'
        ' Basic filters are available for the ID and'
        ' active status of the TransactionReport.'
      ),
      response=TransactionReportGetResponse,
      children={
        model_fields.ID: Schema(
          description='The ID of the TransactionReport in question.',
          types=types.UUID(),
        ),
        transaction_report_fields.IS_ACTIVE: Schema(
          description='The active status of the TransactionReport.',
          types=types.BOOLEAN(),
        ),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    id = self.active_response.force_get_child(model_fields.ID).render()

    queryset = []
    if id is not None:
      queryset = context.get_account().transaction_reports.filter(id=id)
    else:
      is_active = self.active_response.force_get_child(transaction_report_fields.IS_ACTIVE).render()

      if is_active is None:
        queryset = context.get_account().transaction_reports.all()
      else:
        queryset = context.get_account().transaction_reports.filter(is_active=is_active)

    self.active_response.add_internal_queryset(queryset)
