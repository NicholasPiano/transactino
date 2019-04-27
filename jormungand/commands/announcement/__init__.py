
from .constants import announcement_constants
from .get import get

def announcement(args):
  if announcement_constants.GET in args:
    get(args)
