
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import fee_report_constants

def activate(args):
  activate_args = input_args({
    fee_report_constants.FEE_REPORT_ID: {
      method_constants.INPUT: 'Enter the FeeReport ID to activate',
      method_constants.TYPE: str,
    },
    fee_report_constants.IS_ACTIVE: {
      method_constants.INPUT: 'Indicate whether the FeeReport should be active',
      method_constants.TYPE: bool,
    },
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.FEE_REPORT: {
          method_constants.METHODS: {
            fee_report_constants.ACTIVATE: activate_args,
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
    model_constants.FEE_REPORT,
    method_constants.METHODS,
    fee_report_constants.ACTIVATE,
  ])

  print(json.dumps(activate_json, indent=2))
