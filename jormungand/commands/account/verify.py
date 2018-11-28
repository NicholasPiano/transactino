
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers

from .constants import account_constants

def verify(args):
  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.ACCOUNT: {
          method_constants.METHODS: {
            account_constants.VERIFY: {},
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
  verify_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.ACCOUNT,
    method_constants.METHODS,
    account_constants.VERIFY,
  ])

  print(json.dumps(verify_json, indent=2))
