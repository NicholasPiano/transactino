
from .constants import address_constants
from .get import get

def address(args):
  if address_constants.GET in args:
    get(args)
