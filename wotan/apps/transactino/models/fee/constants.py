
from apps.subscription.models.account.constants import account_fields

class fee_report_block_wrapper_prototype_constants:
  pass

class fee_report_block_wrapper_prototype_fields:
  HASH = 'hash'

class fee_report_block_wrapper_constants:
  FEE_REPORT_BLOCK_WRAPPER_TASK = 'fee_report_block_wrapper_task'

class fee_report_block_wrapper_fields:
  HASH = 'hash'
  AVERAGE_TX_FEE = 'average_tx_fee'
  AVERAGE_TX_FEE_DENSITY = 'average_tx_fee_density'
  START_TIME = 'start_time'
  END_TIME = 'end_time'
  IS_PROCESSING = 'is_processing'
  IS_COMPLETE = 'is_complete'

class fee_report_constants:
  ACCOUNT_RELATED_MODEL = 'subscription.Account'
  ACCOUNT_RELATED_NAME = 'fee_reports'
  FEE_REPORT_TASK = 'fee_report_task'

class fee_report_fields:
  ACCOUNT = 'account'
  IS_ACTIVE = 'is_active'
  BLOCKS_TO_INCLUDE = 'blocks_to_include'
  LATEST_BLOCK_HASH = 'latest_block_hash'
  HAS_BEEN_READY = 'has_been_ready'
  HAS_BEEN_RUN = 'has_been_run'
  IS_PROCESSING = 'is_processing'
  AVERAGE_TX_FEE = 'average_tx_fee'
  AVERAGE_TX_FEE_DENSITY = 'average_tx_fee_density'
  LAST_UPDATE_START_TIME = 'last_update_start_time'
  LAST_UPDATE_END_TIME = 'last_update_end_time'

account_fields.FEE_REPORTS = fee_report_constants.ACCOUNT_RELATED_NAME
