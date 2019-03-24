
from ..constants import transaction_report_fields

class transaction_match_constants:
  TRANSACTION_REPORT_RELATED_MODEL = 'transactino.TransactionReport'
  TRANSACTION_REPORT_RELATED_NAME = 'matches'

class transaction_match_fields:
  TRANSACTION_REPORT = 'transaction_report'
  BLOCK_HASH = 'block_hash'
  TXID = 'txid'
  VALUE = 'value'

transaction_report_fields.MATCHES = transaction_match_constants.TRANSACTION_REPORT_RELATED_NAME
