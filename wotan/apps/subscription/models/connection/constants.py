
from ..ip.constants import ip_fields

class close_codes:
  DEAD_HOST = 100

class connection_constants:
  IP_RELATED_MODEL = 'subscription.IP'
  IP_RELATED_NAME = 'connections'

class connection_fields:
  IP_VALUE = 'ip_value'
  IS_ONLINE = 'is_online'
  NAME = 'name'
  CLOSED_AT = 'closed_at'
  CLOSED_WITH_CODE = 'closed_with_code'

ip_fields.CONNECTIONS = connection_constants.IP_RELATED_NAME
