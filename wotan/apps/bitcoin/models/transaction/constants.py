
from ..block.constants import block_fields

class transaction_prototype_constants:
  pass

class transaction_prototype_fields:
  TXID = 'txid'

class transaction_constants:
  BLOCK_RELATED_MODEL = 'bitcoin.Block'
  BLOCK_RELATED_NAME = 'transactions'
  TRANSACTION_TASK = 'transaction_task'

class transaction_fields:
  BLOCK = 'block'
  TXID = 'txid'
  HASH = 'hash'
  SIZE = 'size'
  IS_COMPLETE = 'is_complete'

block_fields.TRANSACTIONS = transaction_constants.BLOCK_RELATED_NAME
