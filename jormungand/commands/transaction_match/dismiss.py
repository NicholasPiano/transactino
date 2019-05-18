
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import transaction_match_constants
from .get import get_args

def dismiss(args):
  dismiss = get_args()

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.TRANSACTION_MATCH: {
          method_constants.METHODS: {
            transaction_match_constants.DISMISS: dismiss,
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

  print(json.dumps(response_json, indent=2))
