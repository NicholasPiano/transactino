
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import payment_constants

def get(args):
  closed = 'closed' in args

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.PAYMENT: {
          method_constants.METHODS: {
            payment_constants.GET: {
              payment_constants.IS_OPEN: not closed,
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

  check_for_announcements(response)

  response_json = json.loads(response.text)
  get_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.PAYMENT,
    model_constants.INSTANCES,
  ])

  print(json.dumps(get_json, indent=2))
