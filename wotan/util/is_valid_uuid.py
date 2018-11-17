
import uuid
from uuid import UUID

def is_valid_uuid(uuid_string):
  if isinstance(uuid_string, str) or isinstance(uuid_string, UUID):
    try:
      if hasattr(uuid_string, 'hex') and is_valid_uuid(uuid_string.hex):
        val = uuid_string
      else:
        val = UUID(uuid_string, version=4)
    except ValueError:
      return False
    return str(val) == uuid_string or val.hex == uuid_string or val == uuid_string
  return False
