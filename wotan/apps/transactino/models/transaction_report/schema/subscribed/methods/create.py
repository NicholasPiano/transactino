
from util.merge import merge
from util.api import (
  Schema, StructureSchema,
  StructureResponse,
  types,
)

from apps.base.schema.constants import schema_constants
from apps.subscription.schema.with_origin import WithOrigin, WithOriginResponse
from apps.subscription.schema.with_challenge import WithChallenge

from ....constants import transaction_report_fields
from .constants import create_constants
from .errors import create_errors

class TransactionReportCreateResponse(StructureResponse, WithOriginResponse):
  pass

class TransactionReportCreateSchema(WithOrigin, WithChallenge, StructureSchema):
  def __init__(self, Model):
    self.model = Model
    super().__init__(
      description=(
        'The schema for the TransactionReport create method.'
      ),
      response=TransactionReportCreateResponse,
      origin=create_constants.ORIGIN,
      children={
        transaction_report_fields.IS_ACTIVE: Schema(
          description=(
            'Whether or not the report should be initially active.'
          ),
          types=types.BOOLEAN(),
        ),
        transaction_report_fields.TARGET_ADDRESS: Schema(
          description=(
            'The address to watch'
          ),
          types=types.STRING(),
        ),
        transaction_report_fields.VALUE_EQUAL_TO: Schema(
          description=(
            'A match will be recorded if the integer Satoshi amount'
            ' of an output to the target address is equal to this value.'
            ' WARNING: cannot be used in conjunction with the value_less_than'
            ' or value_greater_than properties.'
          ),
          types=types.POSITIVE_INTEGER(),
        ),
        transaction_report_fields.VALUE_LESS_THAN: Schema(
          description=(
            'A match will be recorded if the integer Satoshi amount'
            ' of an output to the target address is less than this value,'
            ' depending on the value of the value_greater_than property.'
            ' WARNING: cannot be used in conjunction with the value_equal_to'
            ' property.'
          ),
          types=types.POSITIVE_INTEGER(),
        ),
        transaction_report_fields.VALUE_GREATER_THAN: Schema(
          description=(
            'A match will be recorded if the integer Satoshi amount'
            ' of an output to the target address is greater than this value,'
            ' depending on the value of the value_less_than property.'
            ' WARNING: cannot be used in conjunction with the value_equal_to'
            ' property.'
          ),
          types=types.POSITIVE_INTEGER(),
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        create_errors.TARGET_ADDRESS_NOT_INCLUDED(),
        create_errors.EQUAL_USED_WITH_RANGE(),
        create_errors.EQUAL_OR_RANGE_NOT_INCLUDED(),
        create_errors.INVALID_VALUE_RANGE(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if not passes_pre_response_checks:
      return False

    if transaction_report_fields.TARGET_ADDRESS not in payload:
      self.active_response.add_error(
        create_errors.TARGET_ADDRESS_NOT_INCLUDED(),
      )
      return False

    value_equal_to = transaction_report_fields.VALUE_EQUAL_TO in payload
    value_less_than = transaction_report_fields.VALUE_LESS_THAN in payload
    value_greater_than = transaction_report_fields.VALUE_GREATER_THAN in payload

    if value_equal_to and (value_less_than or value_greater_than):
      self.active_response.add_error(
        create_errors.EQUAL_USED_WITH_RANGE(),
      )
      return False

    value_included = value_equal_to or value_less_than or value_greater_than

    if not value_included:
      self.active_response.add_error(
        create_errors.EQUAL_OR_RANGE_NOT_INCLUDED(),
      )
      return False

    return True

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    value_less_than = self.get_child_value(transaction_report_fields.VALUE_LESS_THAN)
    value_greater_than = self.get_child_value(transaction_report_fields.VALUE_GREATER_THAN)

    if value_less_than is not None and value_greater_than is not None:
      if value_less_than <= value_greater_than:
        self.active_response.add_error(
          create_errors.INVALID_VALUE_RANGE(
            lower_bound=value_greater_than,
            upper_bound=value_less_than,
          ),
        )
        return

    is_active = self.get_child_value(transaction_report_fields.IS_ACTIVE)
    target_address = self.get_child_value(transaction_report_fields.TARGET_ADDRESS)
    value_equal_to = self.get_child_value(transaction_report_fields.VALUE_EQUAL_TO)

    transaction_report = context.get_account().transaction_reports.create(
      is_active=is_active,
      target_address=target_address,
      value_equal_to=value_equal_to,
      value_less_than=value_less_than,
      value_greater_than=value_greater_than or 0,
    )

    self.active_response = self.client.respond(check_challenge=True)
    self.active_response.add_internal_queryset([transaction_report])
