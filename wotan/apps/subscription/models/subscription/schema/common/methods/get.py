
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.constants import model_fields
from apps.base.schema.methods.base import ResponseWithInternalQuerySet

from ....constants import subscription_fields

class SubscriptionGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class SubscriptionGetSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=SubscriptionGetResponse,
      children={
        model_fields.ID: Schema(types=types.UUID()),
        subscription_fields.IS_ACTIVE: Schema(types=types.BOOLEAN()),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    id = self.active_response.force_get_child(model_fields.ID).render()

    queryset = []
    if id is not None:
      queryset = context.get_account().subscriptions.filter(id=id)
    else:
      is_active = self.active_response.force_get_child(subscription_fields.IS_ACTIVE).render()

      if is_active is None:
        queryset = context.get_account().subscriptions.all()
      else:
        queryset = context.get_account().subscriptions.filter(is_active=is_active)

    self.active_response.add_internal_queryset(queryset)
