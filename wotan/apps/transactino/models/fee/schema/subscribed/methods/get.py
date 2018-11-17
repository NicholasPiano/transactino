
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

class FeeReportGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class FeeReportGetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=FeeReportGetResponse,
      children={
        model_fields.ID: Schema(types=types.UUID()),
        fee_report_fields.IS_ACTIVE: Schema(types=types.BOOLEAN()),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    id = self.active_response.force_get_child(model_fields.ID).render()

    queryset = []
    if id is not None:
      queryset = context.get_account().fee_reports.filter(id=id)
    else:
      is_active = self.active_response.force_get_child(fee_report_fields.IS_ACTIVE).render()

      if is_active is None:
        queryset = context.get_account().fee_reports.all()
      else:
        queryset = context.get_account().fee_reports.filter(is_active=is_active)

    self.active_response.add_internal_queryset(queryset)
