
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers

from .constants import fee_report_constants

def delete(args):
  fee_report_id = input('Enter the fee report ID: ')

  delete_request_json = {
    fee_report_constants.FEE_REPORT_ID: fee_report_id,
  }

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.FEE_REPORT: {
          method_constants.METHODS: {
            fee_report_constants.DELETE: delete_request_json,
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

  response_json = json.loads(response.text)
  delete_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.FEE_REPORT,
    method_constants.METHODS,
    fee_report_constants.DELETE,
  ])

  print(json.dumps(delete_json, indent=2))
