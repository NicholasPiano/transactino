
from util.merge import merge
from util.api import (
  Schema, StructureSchema, TemplateSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.constants import model_fields
from apps.base.schema.methods.base import ResponseWithInternalQuerySet

from ....constants import transaction_match_fields
from .constants import get_constants
from .errors import get_errors

class TransactionMatchGetResponse(StructureResponse, ResponseWithInternalQuerySet):
  pass

class TransactionMatchGetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'The schema for the TransactionMatch get method.'
        ' Basic filters are available for the ID and'
        ' active status of the TransactionMatch.'
      ),
      response=TransactionMatchGetResponse,
      children={
        get_constants.TRANSACTION_REPORT_ID: Schema(
          description='Filter by the ID of the parent TransactionReport.',
          types=types.UUID(),
        ),
        get_constants.TRANSACTION_REPORT_TARGET_ADDRESS: Schema(
          description='Filter by the target address of the parent TransactionReport.',
        ),
        get_constants.TRANSACTION_REPORT_IS_ACTIVE: Schema(
          description='Filter by the active status of the parent TransactionReport.',
          types=types.BOOLEAN(),
        ),
        get_constants.TRANSACTION_MATCH_ID: Schema(
          description=(
            'The ID of the TransactionMatch in question. This value'
            ' will override any filters applied.'
          ),
          types=types.UUID(),
        ),
        transaction_match_fields.IS_NEW: Schema(
          description=(
            'Filter by the new status of the TransactionMatch.'
          ),
          types=types.BOOLEAN(),
        ),transaction_match_fields.BLOCK_HASH: Schema(
          description='Filter by the block hash of the TransactionMatch.',
        ),
      },
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        get_errors.TRANSACTION_MATCH_DOES_NOT_EXIST(),
      },
    )

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    transaction_match_id = self.get_child_value(get_constants.TRANSACTION_MATCH_ID)

    queryset = self.model.objects.filter(transaction_report__account=context.get_account())

    if transaction_match_id is not None:
      queryset = queryset.filter(id=transaction_match_id)

      if not queryset:
        self.active_response.add_error(
          get_errors.TRANSACTION_MATCH_DOES_NOT_EXIST(id=transaction_match_id),
        )
        return

      self.active_response.add_internal_queryset(queryset)
      return

    transaction_report_id = self.get_child_value(get_constants.TRANSACTION_REPORT_ID)
    if transaction_report_id is not None:
      queryset = queryset.filter(transaction_report__id=transaction_report_id)

    transaction_report_target_address = self.get_child_value(get_constants.TRANSACTION_REPORT_TARGET_ADDRESS)
    if transaction_report_target_address is not None:
      queryset = queryset.filter(transaction_report__target_address=transaction_report_target_address)

    transaction_report_is_active = self.get_child_value(get_constants.TRANSACTION_REPORT_IS_ACTIVE)
    if transaction_report_is_active is not None:
      queryset = queryset.filter(transaction_report__is_active=transaction_report_is_active)

    is_new = self.get_child_value(transaction_match_fields.IS_NEW)
    if is_new is not None:
      queryset = queryset.filter(is_new=is_new)

    block_hash = self.get_child_value(transaction_match_fields.BLOCK_HASH)
    if block_hash is not None:
      queryset = queryset.filter(block_hash=block_hash)

    self.active_response.add_internal_queryset(queryset)
