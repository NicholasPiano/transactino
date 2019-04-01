
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import ResponseWithExternalQuerySets
from apps.subscription.schema.with_origin import WithOrigin, WithOriginResponse
from apps.subscription.schema.with_challenge import WithChallenge

from .constants import delete_constants
from .errors import delete_errors

class TransactionReportDeleteResponse(StructureResponse, WithOriginResponse):
  pass

class TransactionReportDeleteSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the TransactionReport delete method. The'
        ' value given to this function is the ID of the'
        ' TransactionReport to delete. WARNING: successful execution'
        ' of this function will also cause all related TransactionMatch'
        ' objects to be deleted.'
      ),
      response=TransactionReportDeleteResponse,
      origin=delete_constants.ORIGIN,
      children={
        delete_constants.TRANSACTION_REPORT_ID: Schema(
          description=(
            'The ID of the TransactionReport object to delete.'
          ),
          types=types.UUID(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        delete_errors.TRANSACTION_REPORT_ID_NOT_INCLUDED(),
        delete_errors.TRANSACTION_REPORT_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if delete_constants.TRANSACTION_REPORT_ID not in payload:
      self.active_response.add_error(
        delete_errors.TRANSACTION_REPORT_ID_NOT_INCLUDED(),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    transaction_report_id = self.get_child_value(delete_constants.TRANSACTION_REPORT_ID)

    transaction_report = context.get_account().transaction_reports.get(id=transaction_report_id)
    if transaction_report is None:
      self.active_response.add_error(
        delete_errors.TRANSACTION_REPORT_DOES_NOT_EXIST(id=transaction_report_id),
      )
      return

    transaction_report.delete()

    self.active_response = self.client.respond(check_challenge=True)
