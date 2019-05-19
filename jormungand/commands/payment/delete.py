
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

from .constants import payment_constants

def delete_payment(args):
  delete_args = input_args({
    payment_constants.PAYMENT_ID: {
      method_constants.INPUT: 'Enter the Payment ID to delete',
      method_constants.TYPE: str,
    },
  })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.PAYMENT: {
          method_constants.METHODS: {
            payment_constants.DELETE: delete_args,
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

  if method_constants.ERRORS in response.text:
    print(json.dumps(json.loads(response.text), indent=2))
  else:
    print('Done.')
