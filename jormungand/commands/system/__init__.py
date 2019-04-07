
from .constants import system_constants
from .get import get

def system(args):
  if system_constants.GET in args:
    get(args)
