
from sys import argv
import requests

from commands.constants import commands
from commands.schema import schema
from commands.account import account
from commands.challenge import challenge
from commands.subscription import subscription
from commands.payment import payment
from commands.fee_report import fee_report
from commands.system import system
from commands.address import address
from commands.transaction_report import transaction_report
from commands.transaction_match import transaction_match
from commands.announcement import announcement

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
  elif commands.SYSTEM in args:
    system(args)
  elif commands.ADDRESS in args:
    address(args)
  elif commands.TRANSACTION_REPORT in args:
    transaction_report(args)
  elif commands.TRANSACTION_MATCH in args:
    transaction_match(args)
  elif commands.ANNOUNCEMENT in args:
    announcement(args)

respond(argv[1:])
