
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

from ....constants import fee_report_fields
from .constants import create_constants

class FeeReportCreateClientResponse(StructureResponse, BaseClientResponse):
  pass

class FeeReportCreateClientSchema(WithChallengeClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=FeeReportCreateClientResponse,
      children={
        create_constants.CREATE_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class FeeReportCreateResponse(StructureResponse, WithOriginResponse):
  pass

class FeeReportCreateSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the FeeReport create method.'
      ),
      client=FeeReportCreateClientSchema(),
      origin=create_constants.ORIGIN,
      children={
        fee_report_fields.BLOCKS_TO_INCLUDE: Schema(
          description=(
            'The number of blocks over which to calculate the average.'
          ),
          types=types.INTEGER(),
        ),
        fee_report_fields.IS_ACTIVE: Schema(
          description=(
            'Whether or not the report should be initially active.'
          ),
          types=types.BOOLEAN(),
        ),
      },
    )
    self.response = FeeReportCreateResponse

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if not self.challenge_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            create_constants.CREATE_COMPLETE: False,
          },
          self.get_challenge_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      return

    blocks_to_include = self.active_response.force_get_child(fee_report_fields.BLOCKS_TO_INCLUDE).render()
    is_active = self.active_response.force_get_child(fee_report_fields.IS_ACTIVE).render()
    fee_report = context.get_account().fee_reports.create()

    if blocks_to_include is not None:
      fee_report.blocks_to_include = blocks_to_include

    if is_active is not None:
      fee_report.is_active = is_active

    fee_report.save()

    self.active_response = self.client.respond(
      payload={
        create_constants.CREATE_COMPLETE: True,
      },
    )
    self.active_response.add_internal_queryset(context.get_account().fee_reports.filter(id=fee_report._id))
