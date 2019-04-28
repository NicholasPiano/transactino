
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import fee_report_constants

def get(args):
  fee_report_id = input('Enter fee report ID or leave blank for all: ')
  get = {}
  if fee_report_id:
    get = {
      fee_report_constants.FEE_REPORT_ID: fee_report_id,
    }

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.FEE_REPORT: {
          method_constants.METHODS: {
            fee_report_constants.GET: get,
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

  get_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.FEE_REPORT,
    model_constants.INSTANCES,
  ])

  print(json.dumps(get_json, indent=2))
