
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import transaction_report_constants

def delete(args):
  delete_args = input_args({
    transaction_report_constants.TRANSACTION_REPORT_ID: {
      method_constants.INPUT: 'Enter the TransactionReport ID to delete',
      method_constants.TYPE: str,
    },
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.TRANSACTION_REPORT: {
          method_constants.METHODS: {
            transaction_report_constants.DELETE: delete_args,
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
  delete_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.TRANSACTION_REPORT,
    method_constants.METHODS,
    transaction_report_constants.DELETE,
  ])

  print(json.dumps(delete_json, indent=2))
