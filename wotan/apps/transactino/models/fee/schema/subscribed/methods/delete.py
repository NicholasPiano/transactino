
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import ResponseWithExternalQuerySets
from apps.subscription.schema.with_origin import WithOrigin, WithOriginResponse
from apps.subscription.schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)

from .constants import delete_constants
from .errors import delete_errors

class FeeReportDeleteClientResponse(StructureResponse, ResponseWithExternalQuerySets):
  pass

class FeeReportDeleteClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=FeeReportDeleteClientResponse,
      children={
        delete_constants.DELETE_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class FeeReportDeleteResponse(WithOriginResponse):
  pass

class FeeReportDeleteSchema(WithOrigin, WithChallenge):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      types=types.UUID(),
      client=FeeReportDeleteClientSchema(),
      origin=delete_constants.ORIGIN,
    )
    self.response = FeeReportDeleteResponse

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        delete_errors.FEE_REPORT_DOES_NOT_EXIST(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    if not context.get_account().fee_reports.filter(id=payload).count():
      self.active_response.add_error(
        delete_errors.FEE_REPORT_DOES_NOT_EXIST(id=payload),
      )
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            delete_constants.DELETE_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    fee_report = context.get_account().fee_reports.get(id=payload)
    fee_report.delete()

    self.active_response = self.client.respond(
      payload={
        delete_constants.DELETE_COMPLETE: True,
      },
    )
