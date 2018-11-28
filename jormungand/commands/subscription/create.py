
import json
import requests
from dateutil import parser, tz

import settings
from constants import transactino_constants, model_constants, method_constants
from util.get_path import get_path
from util.make_headers import make_headers

from .constants import subscription_constants

def create(args):
  duration_in_days = input('Enter the number of days the subscription will be active: ')
  activation_date = input('Enter the activation date: ')

  unaware_datetime = parser.parse(activation_date)
  aware_datetime = unaware_datetime.replace(tzinfo=tz.gettz())

  payload = {
    transactino_constants.SCHEMA: {
      model_constants.MODELS: {
        model_constants.SUBSCRIPTION: {
          method_constants.METHODS: {
            subscription_constants.CREATE: {
              subscription_constants.ACTIVATION_DATE: aware_datetime.isoformat(),
              subscription_constants.DURATION_IN_DAYS: duration_in_days,
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
  create_json = get_path(response_json, [
    transactino_constants.SCHEMA,
    model_constants.MODELS,
    model_constants.SUBSCRIPTION,
    method_constants.METHODS,
    subscription_constants.CREATE,
  ])

  print(json.dumps(create_json, indent=2))
