
from ..account.constants import account_fields

class ip_constants:
  ACCOUNT_RELATED_MODEL = 'subscription.Account'
  ACCOUNT_RELATED_NAME = 'ips'

class ip_fields:
  ACCOUNT = 'account'
  VALUE = 'value'
  IS_ONLINE = 'is_online'

account_fields.IPS = ip_constants.ACCOUNT_RELATED_NAME
