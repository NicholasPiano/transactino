
from .constants import challenge_constants
from .get import get
from .respond import respond
from .delete import delete_challenge

def challenge(args):
  if challenge_constants.GET in args:
    get(args)
  elif challenge_constants.RESPOND in args:
    respond(args)
  elif challenge_constants.DELETE in args:
    delete_challenge(args)
