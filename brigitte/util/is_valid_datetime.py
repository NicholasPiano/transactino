
from dateutil.parser import parse

def is_valid_datetime(value):
  try:
    parse(value)
    return True
  except:
    return False
