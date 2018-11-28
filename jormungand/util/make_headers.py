
import json
import requests

def make_headers(url):
  get_response = requests.get(url)
  token = json.loads(get_response.text).get('token')

  headers = {
    'X-CSRFToken': token,
    'Cookie': 'csrftoken={}'.format(token),
    'Content-Type': 'application/json',
  }

  return headers
