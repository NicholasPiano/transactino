
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

def get(args):
  closed = 'closed' in args
  save = 'save' in args

  get_args = input_args({
    challenge_constants.CHALLENGE_ID: {
      method_constants.INPUT: 'Enter the Challenge ID or leave blank for all',
      method_constants.TYPE: str,
    },
  })

  get_args.update({
    challenge_constants.IS_OPEN: not closed,
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.CHALLENGE: {
          method_constants.METHODS: {
            challenge_constants.GET: get_args,
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
    model_constants.CHALLENGE,
    model_constants.INSTANCES,
  ])

  if instances_json is None:
    print(json.dumps(response_json), indent=2)
    return

  for challenge_id, attributes_json in instances_json.items():
    print('Challenge ID: ', challenge_id, '\n')
    encrypted_content = get_path(attributes_json, [
      model_constants.ATTRIBUTES,
      challenge_constants.ENCRYPTED_CONTENT,
    ])
    print(encrypted_content + '\n')

    if save:
      if not exists(settings.CHALLENGE_PATH):
        os.mkdir(settings.CHALLENGE_PATH)

      challenge_path = join(settings.CHALLENGE_PATH, challenge_id)
      if not exists(challenge_path):
        os.mkdir(challenge_path)

      message_path = join(challenge_path, 'message.asc')
      if not exists(message_path):
        with open(message_path, 'w') as message_file:
          message_file.write(encrypted_content)
