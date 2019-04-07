
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers

from .constants import address_constants

def get(args):
  address_id = input('Enter an address ID: ')

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.ADDRESS: {
          method_constants.METHODS: {
            address_constants.GET: {
              address_constants.ADDRESS_ID: address_id,
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
    model_constants.ADDRESS,
    model_constants.INSTANCES,
  ])

  if instances_json is None:
    print(json.dumps(response_json, indent=2))
    return

  print(json.dumps(instances_json, indent=2))
