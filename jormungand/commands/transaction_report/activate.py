
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import transaction_report_constants

active_map = {
  'Y': True,
  'N': False,
}

def get_active():
  return input('Indicate whether the transaction report should be active (Y/N): ')

def activate(args):
  transaction_report_id = input('Enter the transaction report ID: ')

  is_active = get_active()
  while is_active not in active_map:
    is_active = get_active()

  activate_request_json = {
    transaction_report_constants.TRANSACTION_REPORT_ID: transaction_report_id,
    transaction_report_constants.IS_ACTIVE: active_map.get(is_active),
  }

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.TRANSACTION_REPORT: {
          method_constants.METHODS: {
            transaction_report_constants.ACTIVATE: activate_request_json,
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
  activate_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.TRANSACTION_REPORT,
    method_constants.METHODS,
    transaction_report_constants.ACTIVATE,
  ])

  print(json.dumps(activate_json, indent=2))
