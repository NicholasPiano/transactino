
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.base import BaseClientResponse

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from ......schema.with_payment import (
  WithPayment,
  WithPaymentClientSchema,
)
from ....constants import ip_fields
from .constants import create_constants
from .errors import create_errors

class IPCreateClientResponse(StructureResponse, BaseClientResponse):
  pass

class IPCreateClientSchema(WithChallengeClientSchema, WithPaymentClientSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=IPCreateClientResponse,
      children={
        create_constants.CREATE_COMPLETE: Schema(types=types.BOOLEAN()),
      },
    )

class IPCreateResponse(StructureResponse, WithOriginResponse):
  pass

class IPCreateSchema(WithOrigin, WithChallenge, WithPayment, StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      client=IPCreateClientSchema(),
      origin=create_constants.ORIGIN,
      children={
        ip_fields.VALUE: Schema(),
      }
    )
    self.response = IPCreateResponse

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        create_errors.VALUE_NOT_INCLUDED(),
        create_errors.IP_ALREADY_BOUND(),
      },
    )

  def should_check_challenge(self, payload, context):
    return not context.get_account().payments.filter(
      origin=self.origin,
      is_open=False,
      has_been_used=False,
    ).count()

  def should_check_payment(self, payload, context):
    return context.get_account().ips.count() >= create_constants.MAX_IPS

  def get_btc_amount(self, context):
    return create_constants.BEYOND_MAX_COST_PER_IP

  def passes_pre_response_checks(self, payload, context):
    if ip_fields.VALUE not in payload:
      self.active_response.add_error(create_errors.VALUE_NOT_INCLUDED())
      return False

    ip_value = payload.get(ip_fields.VALUE)
    if self.model.objects.filter(value=ip_value).exclude(account=None).exists():
      self.active_response.add_error(create_errors.IP_ALREADY_BOUND(value=ip_value))
      return False

    return super().passes_pre_response_checks(payload, context)

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)
    if self.active_response.has_errors():
      return

    if not self.challenge_accepted or not self.payment_accepted:
      self.active_response = self.client.respond(
        payload=merge(
          {
            create_constants.CREATE_COMPLETE: False,
          },
          self.get_challenge_client_response(),
          self.get_payment_client_response(),
        ),
      )
      self.active_response.add_external_queryset(self.active_challenge_queryset)
      self.active_response.add_external_queryset(self.active_payment_queryset)
      return

    ip_value = self.active_response.get_child(ip_fields.VALUE).render()
    ip, ip_created = context.get_account().ips.get_or_create(value=ip_value)

    self.active_response = self.client.respond(
      payload={
        create_constants.CREATE_COMPLETE: True,
      },
    )
    self.active_response.add_internal_queryset(context.get_account().ips.filter(value=ip_value))
