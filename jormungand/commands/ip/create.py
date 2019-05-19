
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import ip_constants

def create(args):
  print('INFO: Run this method leaving arguments blank to generate a Challenge for this method')
  create_args = input_args({
    ip_constants.VALUE: {
      method_constants.INPUT: 'Enter the value of the IP address',
      method_constants.TYPE: str,
    },
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.IP: {
          method_constants.METHODS: {
            method_constants.CREATE: create_args,
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
    model_constants.IP,
    model_constants.INSTANCES,
  ])

  if not instances_json:
    print(json.dumps(response_json, indent=2))
    return

  print(json.dumps(instances_json, indent=2))
