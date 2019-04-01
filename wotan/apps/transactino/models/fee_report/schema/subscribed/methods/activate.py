
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  Response, StructureResponse,
  types,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import BaseClientResponse
from apps.subscription.schema.with_origin import WithOrigin, WithOriginResponse
from apps.subscription.schema.with_challenge import WithChallenge

from ....constants import fee_report_fields
from .constants import activate_constants
from .errors import activate_errors

class FeeReportActivateResponse(StructureResponse, WithOriginResponse):
  pass

class FeeReportActivateSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the FeeReport activate method.'
      ),
      response=FeeReportActivateResponse,
      origin=activate_constants.ORIGIN,
      children={
        activate_constants.FEE_REPORT_ID: Schema(
          description='The ID of the FeeReport is question.',
          types=types.UUID(),
        ),
        fee_report_fields.IS_ACTIVE: Schema(
          description=(
            'A boolean value that designates whether'
            ' the report should be active.'
          ),
          types=types.BOOLEAN(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        activate_errors.FEE_REPORT_ID_NOT_INCLUDED(),
        activate_errors.FEE_REPORT_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if not activate_constants.FEE_REPORT_ID in payload:
      self.active_response.add_error(
        activate_errors.FEE_REPORT_ID_NOT_INCLUDED(),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    fee_report_id = self.get_child_value(activate_constants.FEE_REPORT_ID)
    is_active = self.get_child_value(fee_report_fields.IS_ACTIVE)

    fee_report = context.get_account().fee_reports.get(id=fee_report_id)
    if fee_report is None:
      self.active_response.add_error(
        activate_errors.FEE_REPORT_DOES_NOT_EXIST(id=fee_report_id),
      )
      return

    fee_report.is_active = is_active if is_active is not None else True
    fee_report.save()

    self.active_response = self.client.respond(check_challenge=True)
    self.active_response.add_internal_queryset([fee_report])
