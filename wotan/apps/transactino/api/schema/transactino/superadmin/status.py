
from util.api import Schema

from .constants import superadmin_constants

class StatusSchema(Schema):
  # 1. empty object -> start process
  # 2. string -> fail first test
  # 3. string -> pass second test
  # 4.
  pass

def should_enter_status_schema(payload, context):
  pass

def strip_access(payload):
  pass
