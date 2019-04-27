
from .constants import account_constants
from .create import create
from .verify import verify
from .delete import delete
from .lock import lock

def account(args):
  if account_constants.CREATE in args:
    create(args)
  if account_constants.VERIFY in args:
    verify(args)
  if account_constants.DELETE in args:
    delete(args)
  if account_constants.LOCK in args:
    lock(args)
