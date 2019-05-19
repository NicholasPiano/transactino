
import json
import requests

import settings
from constants import transactino_constants, model_constants, method_constants
from util.make_headers import make_headers

def remove_descriptions(dictionary):
  if '_children' not in dictionary:
    return dictionary.get('_description')

  children = dictionary.get('_children')
  return {
    key: remove_descriptions(value)
    for key, value
    in children.items()
  }

def schema(args):
  response = requests.post(
    settings.URL,
    headers=make_headers(),
    data='null',
  )

  response_json = json.loads(response.text)

  if 'reduced' in args:
    print(json.dumps(remove_descriptions(response_json), indent=2))
    return

  print(json.dumps(response_json, indent=2))
