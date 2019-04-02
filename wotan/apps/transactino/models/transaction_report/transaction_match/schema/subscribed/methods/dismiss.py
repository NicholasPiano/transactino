
from ....constants import transaction_match_fields
from .get import TransactionMatchGetSchema

class TransactionMatchDismissSchema(TransactionMatchGetSchema):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.description = (
      'The schema for the TransactionMatch dismiss method.'
      ' Filtered match objects will have their is_new property'
      ' set to false.'
    )
    self.children = {
      child_key: child
      for child_key, child
      in self.children.items()
      if child_key != transaction_match_fields.IS_NEW
    }

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    print(self.active_response.internal_queryset)

    for transaction_match in self.active_response.internal_queryset:
      transaction_match.is_new = False
      transaction_match.save()

    self.active_response.internal_queryset = None
