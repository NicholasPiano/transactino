
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import transaction_report_constants

def create(args):
  print('INFO: Run this method leaving arguments blank to generate a Challenge for this method')
  create_args = input_args({
    transaction_report_constants.TARGET_ADDRESS: {
      method_constants.INPUT: 'Enter the target address',
      method_constants.TYPE: str,
    },
    transaction_report_constants.VALUE_EQUAL_TO: {
      method_constants.INPUT: 'Enter value to match equal (leave blank if not required)',
      method_constants.TYPE: int,
    },
    transaction_report_constants.VALUE_LESS_THAN: {
      method_constants.INPUT: 'Enter maximum value (leave blank if not required)',
      method_constants.TYPE: int,
    },
    transaction_report_constants.VALUE_GREATER_THAN: {
      method_constants.INPUT: 'Enter minimum value (leave blank if not required)',
      method_constants.TYPE: int,
    },
  })

  if create_args:
    create_args.update({
      transaction_report_constants.IS_ACTIVE: True,
    })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.TRANSACTION_REPORT: {
          method_constants.METHODS: {
            transaction_report_constants.CREATE: create_args,
          },
        },
      },
    },
  }

  response = requests.post(
    settings.URL,
    headers=make_headers(),
    data=json.dumps(payload),
  )

  check_for_announcements(response)

  print(json.dumps(json.loads(response.text), indent=2))
