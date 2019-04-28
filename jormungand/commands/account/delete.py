
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import account_constants

def delete(args):
  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.ACCOUNT: {
          method_constants.METHODS: {
            account_constants.DELETE: {},
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
  delete_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.ACCOUNT,
    method_constants.METHODS,
    account_constants.DELETE,
  ])

  print(json.dumps(delete_json, indent=2))
