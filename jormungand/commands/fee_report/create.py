
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import fee_report_constants

def create(args):
  print('INFO: Run this method leaving arguments blank to generate a Challenge for this method')
  create_args = input_args({
    fee_report_constants.BLOCKS_TO_INCLUDE: {
      method_constants.INPUT: 'Enter the number of blocks to include in the FeeReport',
      method_constants.TYPE: int,
    },
  })

  if create_args:
    create_args.update({
      fee_report_constants.IS_ACTIVE: True,
    })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.FEE_REPORT: {
          method_constants.METHODS: {
            method_constants.CREATE: create_args,
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

  response_json = json.loads(response.text)
  create_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.FEE_REPORT,
    method_constants.METHODS,
    method_constants.CREATE,
  ])

  print(json.dumps(create_json, indent=2))
