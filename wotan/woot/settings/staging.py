
import os

from woot.settings.common import *

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

LOGGING_PATH = join(dirname(dirname(dirname(abspath(__file__)))), 'log')
if not exists(LOGGING_PATH):
  os.mkdir(LOGGING_PATH)

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse'
    }
  },
  'formatters': {
    'verbose': {
      'format': '{levelname} {asctime} {message}',
      'style': '{',
    },
  },
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
      'filters': ['require_debug_false'],
      'class': 'django.utils.log.AdminEmailHandler'
    },
    'console': {
      'level': 'DEBUG',
      'class': 'logging.StreamHandler'
    },
    'file': {
      'level': 'DEBUG',
      'class': 'logging.FileHandler',
      'filename': join(LOGGING_PATH, 'log'),
      'formatter': 'verbose',
    },
  },
  'loggers': {
    'django.request': {
      'handlers': ['mail_admins', 'console'],
      'level': 'ERROR',
      'propagate': True,
    },
    'django.debug': {
      'handlers': ['file'],
      'level': 'DEBUG',
      'propagate': False,
    },
  }
}

if os.environ.get('RUN_MAIN', 'false') == 'true':
  from relay.scheduler import scheduler
  SCHEDULER = scheduler
  SCHEDULER.remove_all_jobs()
