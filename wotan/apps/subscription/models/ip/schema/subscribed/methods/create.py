
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from ......schema.with_origin import WithOrigin, WithOriginResponse
from ......schema.with_challenge import (
  WithChallenge,
  WithChallengeClientSchema,
)
from ......schema.with_payment import WithPaymentClientSchema
from ......schema.with_fixed_payment import WithFixedPayment
from ....constants import ip_fields
from .constants import create_constants
from .errors import create_errors

class IPCreateClientSchema(WithChallengeClientSchema, WithPaymentClientSchema):
  pass

class IPCreateResponse(StructureResponse, WithOriginResponse):
  pass

class IPCreateSchema(WithOrigin, WithChallenge, WithFixedPayment, StructureSchema):
  def __init__(self, Model):
    self.model = Model
    super().__init__(
      description=(
        'The schema for the IP create method.'
      ),
      origin=create_constants.ORIGIN,
      response=IPCreateResponse,
      client=IPCreateClientSchema(),
      children={
        ip_fields.VALUE: Schema(
          description=(
            'Must be a valid IPv4 address.'
          ),
          types=types.IP_ADDRESS(),
        ),
      }
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        create_errors.VALUE_NOT_INCLUDED(),
        create_errors.IP_ALREADY_BOUND(),
      },
    )

  def should_check_challenge(self, payload, context):
    closed_payment_exists = context.get_account().payments.filter(
      origin=self.origin,
      is_open=False,
      has_been_used=False,
    ).exists()

    if closed_payment_exists:
      return False

    return super().should_check_challenge(payload, context)

  def should_check_payment(self, payload, context):
    if context.get_account().ips.count() < create_constants.MAX_IPS:
      return False

    return super().should_check_payment(payload, context)

  def get_btc_amount(self, context):
    return create_constants.BEYOND_MAX_COST_PER_IP

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if ip_fields.VALUE not in payload:
      self.active_response.add_error(create_errors.VALUE_NOT_INCLUDED())
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    ip_value = self.get_child_value(ip_fields.VALUE)

    ip = context.get_account().ips.get(value=ip_value)

    if ip is not None:
      self.active_response.add_error(create_errors.IP_ALREADY_BOUND(value=ip_value))
      return

    check_payment = self.should_check_payment(payload, context)

    ip = context.get_account().ips.create(value=ip_value)

    self.active_response = self.client.respond(check_challenge=True, check_payment=check_payment)
    self.active_response.add_internal_queryset([ip])
