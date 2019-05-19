
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import transaction_match_constants

get_config = {
  transaction_match_constants.TRANSACTION_MATCH_ID: {
    method_constants.INPUT: 'Enter transaction match ID or leave blank for all',
    method_constants.TYPE: str,
  },
  transaction_match_constants.TRANSACTION_REPORT_ID: {
    method_constants.INPUT: 'Enter the ID of the parent TransactionReport',
    method_constants.TYPE: str,
  },
  transaction_match_constants.TRANSACTION_REPORT_TARGET_ADDRESS: {
    method_constants.INPUT: 'Enter the target address of the parent TransactionReport',
    method_constants.TYPE: str,
  },
  transaction_match_constants.TRANSACTION_REPORT_IS_ACTIVE: {
    method_constants.INPUT: 'Enter the active status of the parent TransactionReport',
    method_constants.TYPE: bool,
  },
  transaction_match_constants.IS_NEW: {
    method_constants.INPUT: 'Enter the new status of the TransactionMatch',
    method_constants.TYPE: bool,
  },
  transaction_match_constants.BLOCK_HASH: {
    method_constants.INPUT: 'Enter the block hash of the TransactionMatch',
    method_constants.TYPE: str,
  },
}

def get(args):
  get_args = input_args(get_config)

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.TRANSACTION_MATCH: {
          method_constants.METHODS: {
            transaction_match_constants.GET: get_args,
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
    model_constants.TRANSACTION_MATCH,
    model_constants.INSTANCES,
  ])

  if instances_json is None:
    print(json.dumps(response_json, indent=2))
    return

  print(json.dumps(instances_json, indent=2))
