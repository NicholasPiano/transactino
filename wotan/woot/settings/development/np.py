
import os
from os.path import join, dirname, abspath, exists, normpath

from ..scheduler import scheduler
from .common import *

DEBUG = False

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'db',
    'USER': 'transactino',
    'PASSWORD': '3b12e2660df54da2985c3e9e7ef89c43',
    'HOST': 'localhost',
    'PORT': '',
  }
}

if os.environ.get('RUN_MAIN', 'false') == 'true':
  SCHEDULER = scheduler
