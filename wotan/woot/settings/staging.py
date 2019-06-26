
import os

from woot.settings.common import *

if not os.environ.get('IN_SHELL', 'false') == 'true':
  from .scheduler import scheduler
  SCHEDULER = scheduler

DEBUG = False

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'db',
    'USER': 'transactino',
    'PASSWORD': '7737d16e80d744b984b17c1918b81cee',
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
      'handlers': ['mail_admins', 'console', 'file'],
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

ALLOWED_HOSTS = (
  '18.130.90.221',
)
