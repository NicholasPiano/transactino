
import json
import requests
import os
from os.path import exists, join

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import challenge_constants

def delete_challenge(args):
  delete_args = input_args({
    challenge_constants.CHALLENGE_ID: {
      method_constants.INPUT: 'Enter the Challenge ID to delete',
      method_constants.TYPE: str,
    },
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.CHALLENGE: {
          method_constants.METHODS: {
            challenge_constants.DELETE: delete_args,
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

  if method_constants.ERRORS in response.text:
    print(json.dumps(json.loads(response.text), indent=2))
  else:
    print('Done.')
