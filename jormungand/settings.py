
import json

with open('./env.json') as env_file:
  env_data = json.loads(env_file.read())

URL = env_data.get('url')
PUBLIC_KEY_PATH = env_data.get('public_key')
CHALLENGE_PATH = env_data.get('challenge_path')

with open(PUBLIC_KEY_PATH) as public_key_file:
  public_key = public_key_file.read()

PUBLIC_KEY = public_key
