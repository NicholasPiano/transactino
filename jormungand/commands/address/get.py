
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import address_constants

def get(args):
  get_args = input_args({
    address_constants.ADDRESS_ID: {
      method_constants.INPUT: 'Enter an Address ID',
      method_constants.TYPE: str,
    },
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.ADDRESS: {
          method_constants.METHODS: {
            address_constants.GET: get_args,
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
    model_constants.ADDRESS,
    model_constants.INSTANCES,
  ])

  if instances_json is None:
    print(json.dumps(response_json, indent=2))
    return

  print(json.dumps(instances_json, indent=2))
