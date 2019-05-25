
import json
import requests
from dateutil import parser, tz

import settings
from constants import transactino_constants, model_constants, method_constants
from util.input_args import input_args
from util.get_path import get_path
from util.make_headers import make_headers
from util.check_for_announcements import check_for_announcements

from .constants import subscription_constants

def create(args):
  print('INFO: Run this method leaving arguments blank to generate a Challenge for this method')
  create_args = input_args({
    subscription_constants.ACTIVATION_DATE: {
      method_constants.INPUT: 'Enter the activation date',
      method_constants.TYPE: str,
    },
    subscription_constants.DURATION_IN_DAYS: {
      method_constants.INPUT: 'Enter the number of days the Subscription will be active',
      method_constants.TYPE: int,
    },
  })

  if subscription_constants.ACTIVATION_DATE in create_args:
    activation_date = create_args.get(subscription_constants.ACTIVATION_DATE)
    unaware_datetime = parser.parse(activation_date)
    aware_datetime = unaware_datetime.replace(tzinfo=tz.gettz())
    iso_datetime = aware_datetime.isoformat()

    create_args.update({
      subscription_constants.ACTIVATION_DATE: iso_datetime,
    })

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.SUBSCRIPTION: {
          method_constants.METHODS: {
            subscription_constants.CREATE: create_args,
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
  create_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.SUBSCRIPTION,
    method_constants.METHODS,
    subscription_constants.CREATE,
  ])

  print(json.dumps(create_json, indent=2))
