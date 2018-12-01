
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers

from .constants import subscription_constants

def get(args):
  inactive = 'inactive' in args

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.SUBSCRIPTION: {
          method_constants.METHODS: {
            subscription_constants.GET: {
              subscription_constants.IS_ACTIVE: not inactive,
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
  instances_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.SUBSCRIPTION,
    model_constants.INSTANCES,
  ])

  print(json.dumps(instances_json, indent=2))
