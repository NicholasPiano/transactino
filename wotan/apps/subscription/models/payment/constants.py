
from ..account.constants import account_fields
from ..address.constants import address_fields

class payment_constants:
  ACCOUNT_RELATED_MODEL = 'subscription.Account'
  ACCOUNT_RELATED_NAME = 'payments'
  ADDRESS_RELATED_MODEL = 'subscription.Address'
  ADDRESS_RELATED_NAME = 'payments_received'
  PAYMENT_TASK = 'payment_task'

class payment_fields:
  ACCOUNT = 'account'
  ADDRESS = 'address'
  ORIGIN = 'origin'
  IS_OPEN = 'is_open'
  HAS_BEEN_USED = 'has_been_used'
  TIME_CONFIRMED = 'time_confirmed'
  BASE_AMOUNT = 'base_amount'
  UNIQUE_BTC_AMOUNT = 'unique_btc_amount'
  FULL_BTC_AMOUNT = 'full_btc_amount'
  BLOCK_HASH = 'block_hash'
  TXID = 'txid'

account_fields.PAYMENTS = payment_constants.ACCOUNT_RELATED_NAME
address_fields.PAYMENTS_RECEIVED = payment_constants.ADDRESS_RELATED_NAME
