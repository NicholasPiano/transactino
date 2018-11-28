
from .constants import subscription_constants
from .create import create
from .activate import activate

def subscription(args):
  if subscription_constants.CREATE in args:
    create(args)
  if subscription_constants.ACTIVATE in args:
    activate(args)
