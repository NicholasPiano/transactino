
from apps.subscription.models.account.constants import account_fields

class transaction_report_constants:
  ACCOUNT_RELATED_MODEL = 'subscription.Account'
  ACCOUNT_RELATED_NAME = 'transaction_reports'
  TRANSACTION_REPORT_TASK = 'transaction_report_task'

class transaction_report_fields:
  ACCOUNT = 'account'
  IS_ACTIVE = 'is_active'
  TARGET_ADDRESS = 'target_address'
  VALUE_EQUAL_TO = 'value_equal_to'
  VALUE_GREATER_THAN = 'value_greater_than'
  VALUE_LESS_THAN = 'value_less_than'
  LATEST_BLOCK_HASH = 'latest_block_hash'

account_fields.TRANSACTION_REPORTS = transaction_report_constants.ACCOUNT_RELATED_NAME
