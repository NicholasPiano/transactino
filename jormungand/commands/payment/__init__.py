
from .constants import payment_constants
from .get import get

def payment(args):
  if payment_constants.GET in args:
    get(args)
