
import json

from constants import transactino_constants

def check_for_announcements(response):
  response_json = json.loads(response.text)
  announcements = get_path(response_json, [
    transactino_constants.SCHEMA,
    transactino_constants.ANNOUNCEMENTS,
  ])

  if announcements is not None:
    print('ATTENTION: {}'.format(json.dumps(announcements)))
