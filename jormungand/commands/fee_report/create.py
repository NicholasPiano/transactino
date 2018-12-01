
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers

from .constants import fee_report_constants

def create(args):
  blocks_to_include = input('Enter the number of blocks to include in the report: ')

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.FEE_REPORT: {
          method_constants.METHODS: {
            fee_report_constants.CREATE: {
              fee_report_constants.BLOCKS_TO_INCLUDE: int(blocks_to_include),
              'is_active': True,
            },
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
  create_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.FEE_REPORT,
    method_constants.METHODS,
    fee_report_constants.CREATE,
  ])

  print(json.dumps(create_json, indent=2))
