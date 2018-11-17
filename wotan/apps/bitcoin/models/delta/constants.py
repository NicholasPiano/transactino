
from ..transaction.constants import transaction_fields
from ..address.constants import address_fields

class delta_prototype_constants:
  pass

class delta_prototype_fields:
  TXID = 'txid'
  INDEX = 'index'

class delta_constants:
  FROM_TRANSACTION_RELATED_MODEL = 'bitcoin.Transaction'
  FROM_TRANSACTION_RELATED_NAME = 'outgoing_deltas'
  TO_TRANSACTION_RELATED_MODEL = 'bitcoin.Transaction'
  TO_TRANSACTION_RELATED_NAME = 'incoming_deltas'
  ADDRESSES_RELATED_MODEL = 'bitcoin.Address'
  ADDRESSES_RELATED_NAME = 'deltas'
  DELTA_TASK = 'delta_task'

class delta_fields:
  FROM_TRANSACTION = 'from_transaction'
  TO_TRANSACTION = 'to_transaction'
  ADDRESSES = 'addresses'
  TXID = 'txid'
  VALUE = 'value'
  INDEX = 'index'
  IS_COMPLETE = 'is_complete'

transaction_fields.OUTGOING_DELTAS = delta_constants.FROM_TRANSACTION_RELATED_NAME
transaction_fields.INCOMING_DELTAS = delta_constants.TO_TRANSACTION_RELATED_NAME
address_fields.DELTAS = delta_constants.ADDRESSES_RELATED_NAME
