
from ..account.constants import account_fields
from ..address.constants import address_fields

class payment_constants:
  ACCOUNT_RELATED_MODEL = 'subscription.Account'
  ACCOUNT_RELATED_NAME = 'payments'
  TO_ADDRESS_RELATED_MODEL = 'subscription.Address'
  TO_ADDRESS_RELATED_NAME = 'payments_received'
  FROM_ADDRESS_RELATED_MODEL = 'subscription.Address'
  FROM_ADDRESS_RELATED_NAME = 'payments_sent'
  PAYMENT_TASK = 'payment_task'

class payment_fields:
  ACCOUNT = 'account'
  TO_ADDRESS = 'to_address'
  FROM_ADDRESS = 'from_address'
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
address_fields.PAYMENTS_RECEIVED = payment_constants.TO_ADDRESS_RELATED_NAME
address_fields.PAYMENTS_SENT = payment_constants.FROM_ADDRESS_RELATED_NAME
