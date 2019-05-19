
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import fee_report_constants

def get(args):
  get_args = input_args({
    fee_report_constants.FEE_REPORT_ID: {
      method_constants.INPUT: 'Enter the FeeReport ID or leave blank for all',
      method_constants.TYPE: str,
    },
    fee_report_constants.IS_ACTIVE: {
      method_constants.INPUT: 'Enter the active status of the FeeReport',
      method_constants.TYPE: bool,
    },
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.FEE_REPORT: {
          method_constants.METHODS: {
            method_constants.GET: get_args,
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
  instances_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.FEE_REPORT,
    model_constants.INSTANCES,
  ])

  if not instances_json:
    print(json.dumps(response_json, indent=2))
    return

  print(json.dumps(get_json, indent=2))
