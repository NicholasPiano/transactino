
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import transaction_report_constants

def create(args):
  target_address = input('Enter the target address: ')
  value_equal_to = input('Enter value to match equal (leave blank if not required): ')
  value_less_than = input('Enter maximum value (leave blank if not required): ')
  value_greater_than = input('Enter minimum value (leave blank if not required): ')

  create_request_json = {
    transaction_report_constants.TARGET_ADDRESS: target_address,
    transaction_report_constants.IS_ACTIVE: True,
  }

  if value_equal_to:
    create_request_json.update({
      transaction_report_constants.VALUE_EQUAL_TO: value_equal_to,
    })

  else:
    if value_less_than:
      create_request_json.update({
        transaction_report_constants.VALUE_LESS_THAN: value_less_than,
      })

    if value_greater_than:
      create_request_json.update({
        transaction_report_constants.VALUE_GREATER_THAN: value_greater_than,
      })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.TRANSACTION_REPORT: {
          method_constants.METHODS: {
            transaction_report_constants.CREATE: create_request_json,
          },
        },
      },
    },
  }

  response = requests.post(
    settings.URL,
    headers=make_headers(settings.URL),
    data=json.dumps(payload),
  )

  check_for_announcements(response)

  response_json = json.loads(response.text)
  create_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.TRANSACTION_REPORT,
    method_constants.METHODS,
    transaction_report_constants.CREATE,
  ])

  print(json.dumps(create_json, indent=2))
