
import os
from os.path import join, dirname, abspath, exists, normpath

from .common import *

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
