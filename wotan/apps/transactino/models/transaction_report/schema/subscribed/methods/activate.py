
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import BaseClientResponse
from apps.subscription.schema.with_origin import WithOrigin, WithOriginResponse
from apps.subscription.schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)

from ....constants import transaction_report_fields
from .constants import activate_constants
from .errors import activate_errors

class TransactionReportActivateClientResponse(StructureResponse, BaseClientResponse):
  pass

class TransactionReportActivateClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=TransactionReportActivateClientResponse,
      children={
        activate_constants.ACTIVATE_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class TransactionReportActivateResponse(StructureResponse, WithOriginResponse):
  pass

class TransactionReportActivateSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the TransactionReport activate method.'
      ),
      client=TransactionReportActivateClientSchema(),
      origin=activate_constants.ORIGIN,
      children={
        activate_constants.TRANSACTION_REPORT_ID: Schema(
          description='The ID of the TransactionReport is question.',
          types=types.UUID(),
        ),
        transaction_report_fields.IS_ACTIVE: Schema(
          description=(
            'A boolean value that designates whether'
            ' the report should be active.'
          ),
          types=types.BOOLEAN(),
        ),
      },
    )
    self.response = TransactionReportActivateResponse

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        activate_errors.TRANSACTION_REPORT_ID_NOT_INCLUDED(),
        activate_errors.TRANSACTION_REPORT_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if not activate_constants.TRANSACTION_REPORT_ID in payload:
      self.active_response.add_error(
        activate_errors.TRANSACTION_REPORT_ID_NOT_INCLUDED(),
      )
      return False

    transaction_report_id = payload.get(activate_constants.TRANSACTION_REPORT_ID)

    if not context.get_account().transaction_reports.filter(id=transaction_report_id).count():
      self.active_response.add_error(
        activate_errors.TRANSACTION_REPORT_DOES_NOT_EXIST(id=transaction_report_id),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            activate_constants.ACTIVATE_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    transaction_report_id = self.active_response.force_get_child(activate_constants.TRANSACTION_REPORT_ID).render()
    is_active = self.active_response.force_get_child(transaction_report_fields.IS_ACTIVE).render()

    transaction_report = context.get_account().transaction_reports.get(id=transaction_report_id)
    transaction_report.is_active = is_active if is_active is not None else True
    transaction_report.save()

    if transaction_report.is_active:
      transaction_report.schedule_process()
    else:
      transaction_report.unschedule()

    self.active_response = self.client.respond(
      payload={
        activate_constants.ACTIVATE_COMPLETE: True,
      },
    )
    self.active_response.add_internal_queryset(context.get_account().transaction_reports.filter(id=transaction_report._id))
