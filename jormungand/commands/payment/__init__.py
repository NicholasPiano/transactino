
from .constants import payment_constants
from .get import get
from .delete import delete

def payment(args):
  if payment_constants.GET in args:
    get(args)
  if payment_constants.DELETE in args:
    delete(args)
