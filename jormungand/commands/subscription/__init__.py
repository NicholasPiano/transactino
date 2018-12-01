
from .constants import subscription_constants
from .create import create
from .activate import activate
from .get import get

def subscription(args):
  if subscription_constants.CREATE in args:
    create(args)
  if subscription_constants.ACTIVATE in args:
    activate(args)
  if subscription_constants.GET in args:
    get(args)
