
from ..system.constants import system_fields

class announcement_constants:
  SYSTEM_RELATED_MODEL = 'subscription.System'
  SYSTEM_RELATED_NAME = 'announcements'

class announcement_fields:
  SYSTEM = 'system'
  MATTER = 'matter'
  SIGNATURE = 'signature'
  IS_ACTIVE = 'is_active'
  DATE_ACTIVATED = 'date_activated'

system_fields.ANNOUNCEMENTS = announcement_constants.SYSTEM_RELATED_NAME
