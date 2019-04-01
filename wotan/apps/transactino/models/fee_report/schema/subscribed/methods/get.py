
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.constants import model_fields
from apps.base.schema.methods.base import ResponseWithInternalQuerySet

from ....constants import fee_report_fields
from .constants import get_constants

class FeeReportGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class FeeReportGetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the FeeReport get method.'
        ' Basic filters are available for the ID and'
        ' active status of the FeeReport.'
      ),
      response=FeeReportGetResponse,
      children={
        get_constants.FEE_REPORT_ID: Schema(
          description='The ID of the FeeReport in question.',
          types=types.UUID(),
        ),
        fee_report_fields.IS_ACTIVE: Schema(
          description='The active status of the FeeReport.',
          types=types.BOOLEAN(),
        ),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    fee_report_id = self.get_child_value(get_constants.FEE_REPORT_ID)

    queryset = []
    if fee_report_id is not None:
      queryset = context.get_account().fee_reports.filter(id=fee_report_id)
    else:
      is_active = self.get_child_value(fee_report_fields.IS_ACTIVE)

      if is_active is None:
        queryset = context.get_account().fee_reports.all()
      else:
        queryset = context.get_account().fee_reports.filter(is_active=is_active)

    self.active_response.add_internal_queryset(queryset)
