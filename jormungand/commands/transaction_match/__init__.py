
from .constants import transaction_match_constants
from .get import get
from .dismiss import dismiss

def transaction_match(args):
  if transaction_match_constants.GET in args:
    get(args)
  if transaction_match_constants.DISMISS in args:
    dismiss(args)
