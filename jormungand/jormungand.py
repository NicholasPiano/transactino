
from sys import argv
import requests

from commands.constants import commands
from commands.schema import schema
from commands.account import account
from commands.challenge import challenge

def respond(args):
  if commands.ACCOUNT in args:
    account(args)
  elif commands.SCHEMA in args:
    schema(args)
  elif commands.CHALLENGE in args:
    challenge(args)

respond(argv[1:])
