
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
from .constants import get_constants
from .errors import get_errors

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
        get_constants.TRANSACTION_REPORT_ID: Schema(
          description='The ID of the TransactionReport in question.',
          types=types.UUID(),
        ),
        transaction_report_fields.IS_ACTIVE: Schema(
          description='The active status of the TransactionReport.',
          types=types.BOOLEAN(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.TRANSACTION_REPORT_DOES_NOT_EXIST(),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    transaction_report_id = self.get_child_value(get_constants.TRANSACTION_REPORT_ID)

    if transaction_report_id is not None:
      queryset = context.get_account().transaction_reports.filter(id=transaction_report_id)

      if not queryset:
        self.active_response.add_error(
          get_errors.TRANSACTION_REPORT_DOES_NOT_EXIST(id=transaction_report_id),
        )
        return

      self.active_response.add_internal_queryset(queryset)
      return

    is_active = self.get_child_value(transaction_report_fields.IS_ACTIVE)

    queryset = (
      context.get_account().transaction_reports.all()
      if is_active is None
      else context.get_account().transaction_reports.filter(is_active=is_active)
    )

    self.active_response.add_internal_queryset(queryset)
