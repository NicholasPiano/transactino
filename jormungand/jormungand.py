
from sys import argv
import requests

from commands.constants import commands
from commands.schema import schema
from commands.account import account
from commands.challenge import challenge
from commands.subscription import subscription
from commands.payment import payment
from commands.fee_report import fee_report

def respond(args):
  if commands.ACCOUNT in args:
    account(args)
  elif commands.SCHEMA in args:
    schema(args)
  elif commands.CHALLENGE in args:
    challenge(args)
  elif commands.SUBSCRIPTION in args:
    subscription(args)
  elif commands.PAYMENT in args:
    payment(args)
  elif commands.FEE_REPORT in args:
    fee_report(args)

respond(argv[1:])
