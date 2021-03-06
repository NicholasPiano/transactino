
import json
import requests
from os.path import exists, join

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import challenge_constants

def respond(args):
  read = 'read' in args

  respond_args = input_args({
    challenge_constants.CHALLENGE_ID: {
      method_constants.INPUT: 'Enter the Challenge ID to respond to',
      method_constants.TYPE: str,
    },
  })

  if not read:
    content = input(
      (
        'Please enter the decrypted string that has been'
        ' re-encrypted to the public key of the System model.'
        ' It should be in ASCII armor format with any newlines'
        ' replaced with their escaped equivalents (\\n). This is'
        ' for the purposes of pasting the text into the command line: \n\n'
      ),
    )

  if read:
    challenge_id = respond_args.get(challenge_constants.CHALLENGE_ID)
    challenge_path = join(settings.CHALLENGE_PATH, challenge_id)
    if not exists(challenge_path):
      print('Cannot find saved challenge directory...')
      return

    encrypted_content_path = join(challenge_path, 'encrypted.asc')
    if not exists(encrypted_content_path):
      print('Cannot find file {}/encrypted.asc'.format(challenge_id))
      return

    with open(encrypted_content_path, 'r') as encrypted_content_file:
      content = encrypted_content_file.read()

  respond_args.update({
    challenge_constants.CONTENT: content,
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.CHALLENGE: {
          method_constants.METHODS: {
            challenge_constants.RESPOND: respond_args,
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
  respond_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.CHALLENGE,
    method_constants.METHODS,
    challenge_constants.RESPOND,
  ])

  print(json.dumps(respond_json, indent=2))
