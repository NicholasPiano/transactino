
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import system_constants

def get(args):
  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.SYSTEM: {
          method_constants.METHODS: {
            system_constants.GET: {},
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
  instances_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.SYSTEM,
    model_constants.INSTANCES,
  ])

  if instances_json is None:
    print(json.dumps(response_json, indent=2))
    return

  for system_id, attributes_json in instances_json.items():
    print('System ID: ', system_id, '\n')

    public_key = get_path(attributes_json, [
      model_constants.ATTRIBUTES,
      system_constants.PUBLIC_KEY,
    ])

    print('PUBLIC KEY:')
    print(public_key + '\n')
    print('--------')

    guarantee = get_path(attributes_json, [
      model_constants.ATTRIBUTES,
      system_constants.GUARANTEE,
    ])

    print('GUARANTEE')
    print(guarantee + '\n')
    print('--------')

    guarantee_signature = get_path(attributes_json, [
      model_constants.ATTRIBUTES,
      system_constants.GUARANTEE_SIGNATURE,
    ])

    print('GUARANTEE SIGNATURE')
    print(guarantee_signature + '\n')
    print('--------')

    disclaimer = get_path(attributes_json, [
      model_constants.ATTRIBUTES,
      system_constants.DISCLAIMER,
    ])

    print('DISCLAIMER')
    print(disclaimer + '\n')
    print('--------')

    disclaimer_signature = get_path(attributes_json, [
      model_constants.ATTRIBUTES,
      system_constants.DISCLAIMER_SIGNATURE,
    ])
    
    print('DISCLAIMER SIGNATURE')
    print(disclaimer_signature + '\n')
    print('--------')
