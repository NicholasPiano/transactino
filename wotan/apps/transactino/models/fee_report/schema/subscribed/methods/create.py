
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from apps.base.schema.constants import schema_constants
from apps.subscription.schema.with_origin import WithOrigin, WithOriginResponse
from apps.subscription.schema.with_challenge import WithChallenge

from ....constants import fee_report_fields
from .constants import create_constants

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
      response=FeeReportCreateResponse,
      origin=create_constants.ORIGIN,
      children={
        fee_report_fields.BLOCKS_TO_INCLUDE: Schema(
          description=(
            'The number of blocks over which to calculate the average.'
            ' Defaults to 1 if omitted.'
          ),
          types=types.INTEGER(),
        ),
        fee_report_fields.IS_ACTIVE: Schema(
          description=(
            'Whether or not the report should be initially active.'
            ' Defaults to true if omitted.'
          ),
          types=types.BOOLEAN(),
        ),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    blocks_to_include = self.get_child_value(fee_report_fields.BLOCKS_TO_INCLUDE)
    is_active = self.get_child_value(fee_report_fields.IS_ACTIVE)

    fee_report = context.get_account().fee_reports.create(
      blocks_to_include=blocks_to_include if blocks_to_include is not None else 1,
      is_active=is_active if is_active is not None else True,
    )

    self.active_response = self.client.respond()
    self.active_response.add_internal_queryset([fee_report])
