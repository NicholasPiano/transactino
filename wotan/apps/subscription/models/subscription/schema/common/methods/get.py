
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
from .constants import get_constants
from .errors import get_errors

class SubscriptionGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class SubscriptionGetSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'The schema for the Subscription get method.'
        ' Filters can be applied for the active status'
        ' and the ID of the subscription.'
      ),
      response=SubscriptionGetResponse,
      children={
        get_constants.SUBSCRIPTION_ID: Schema(
          description=(
            'The subscription ID'
          ),
          types=types.UUID(),
        ),
        subscription_fields.IS_ACTIVE: Schema(
          description=(
            'The subscription active status. If omitted, all subscriptions'
            ' are returned.'
          ),
          types=types.BOOLEAN(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.SUBSCRIPTION_DOES_NOT_EXIST(),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    subscription_id = self.get_child_value(get_constants.SUBSCRIPTION_ID)

    queryset = []
    if subscription_id is not None:
      queryset = context.get_account().subscriptions.filter(id=subscription_id)

      if not queryset:
        self.active_response.add_error(
          get_errors.SUBSCRIPTION_DOES_NOT_EXIST(id=subscription_id)
        )
        return

    else:
      is_active = self.get_child_value(subscription_fields.IS_ACTIVE)

      if is_active is None:
        queryset = context.get_account().subscriptions.all()
      else:
        queryset = context.get_account().subscriptions.filter(is_active=is_active)

    self.active_response.add_internal_queryset(queryset)
