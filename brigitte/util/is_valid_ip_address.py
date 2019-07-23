
import re

def is_valid_ip_address(string):
  if not isinstance(string, str):
    return False

  search = re.search('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', string)

  return search is not None
