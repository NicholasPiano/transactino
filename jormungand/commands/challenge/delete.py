
import json
import requests
import os
from os.path import exists, join

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers

from .constants import challenge_constants

def delete_challenge(args):
  challenge_id = input('Enter a challenge ID: ')

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.CHALLENGE: {
          method_constants.METHODS: {
            challenge_constants.DELETE: {
              challenge_constants.CHALLENGE_ID: challenge_id,
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

  if '_errors' in response.text:
    print(json.dumps(json.loads(response_json), indent=2))
  else:
    print('Done.')
