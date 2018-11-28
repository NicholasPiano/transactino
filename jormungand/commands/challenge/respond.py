
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers

from .constants import challenge_constants

def respond(args):
  challenge_id = input('Please enter a challenge ID: ')
  plaintext = input('Please enter the decrypted string: ')

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.CHALLENGE: {
          method_constants.METHODS: {
            challenge_constants.RESPOND: {
              challenge_constants.CHALLENGE_ID: challenge_id,
              challenge_constants.PLAINTEXT: plaintext,
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
  respond_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.CHALLENGE,
    method_constants.METHODS,
    challenge_constants.RESPOND,
  ])

  print(json.dumps(respond_json, indent=2))
