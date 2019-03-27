
from ..account.constants import account_fields

class subscription_constants:
  ACCOUNT_RELATED_MODEL = 'subscription.Account'
  ACCOUNT_RELATED_NAME = 'subscriptions'
  DEFAULT_COST_PER_DAY = 40000
  SUBSCRIPTION_TASK = 'subscription_task'

class subscription_fields:
  ACCOUNT = 'account'
  ORIGIN = 'origin'
  DURATION_IN_DAYS = 'duration_in_days'
  ACTIVATION_DATE = 'activation_date'
  IS_VALID_UNTIL = 'is_valid_until'
  HAS_BEEN_ACTIVATED = 'has_been_activated'
  IS_ACTIVE = 'is_active'
  LAST_UPDATE_TIME = 'last_update_time'
  IS_CONTRACT_SIGNED = 'is_contract_signed'
  CONTRACT = 'contract'
  CONTRACT_CLIENT_SIGNATURE = 'contract_client_signature'
  CONTRACT_SYSTEM_SIGNATURE = 'contract_system_signature'

account_fields.SUBSCRIPTIONS = subscription_constants.ACCOUNT_RELATED_NAME
