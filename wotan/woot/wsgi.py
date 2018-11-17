
import os
from django.core.wsgi import get_wsgi_application
import json

with open('./env.json') as env_file:
  env_data = json.loads(env_file.read())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env_data.get('settings'))

application = get_wsgi_application()
