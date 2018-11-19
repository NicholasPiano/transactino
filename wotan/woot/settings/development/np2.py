
import os
from os.path import join, dirname, abspath, exists, normpath

from .common import *

DB_PATH = join(WOOT_PATH, 'db')
if not exists(DB_PATH):
  os.mkdir(DB_PATH)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': join(DB_PATH, 'db.sqlite3'),
  }
}
