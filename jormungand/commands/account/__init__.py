
from .constants import account_constants
from .create import create
from .verify import verify

def account(args):
  if account_constants.CREATE in args:
    create(args)
  if account_constants.VERIFY in args:
    verify(args)
