
import json
import os
from os.path import join, dirname, abspath, exists, normpath
from sys import path

with open('./env.json') as env_file:
  env_data = json.loads(env_file.read())

DEBUG = True

DJANGO_PATH = dirname(dirname(dirname(abspath(__file__))))

APPS_PATH = join(DJANGO_PATH, 'apps')

WOOT_PATH = dirname(dirname(abspath(__file__)))

MEDIA_PATH = join(WOOT_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = join(WOOT_PATH, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
  normpath(join(WOOT_PATH, 'assets')),
)
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

GPG_PATH = join(WOOT_PATH, 'gpg')
if not exists(GPG_PATH):
  os.mkdir(GPG_PATH)

GPG_BINARY = env_data.get('gpg_binary')

KEY_PATH = join(WOOT_PATH, 'keys')
PUBLIC_KEY_TEMPLATE = '{}_public_key.asc'
PRIVATE_KEY_TEMPLATE = '{}_private_key.asc'
TEST_KEY = 'test'
TEST_SYSTEM_KEY = 'test_system'

with open(join(KEY_PATH, TEST_KEY, PUBLIC_KEY_TEMPLATE.format(TEST_KEY)), 'r') as public_key_file:
  test_public_key = public_key_file.read()

with open(join(KEY_PATH, TEST_KEY, PRIVATE_KEY_TEMPLATE.format(TEST_KEY)), 'r') as private_key_file:
  test_private_key = private_key_file.read()

TEST_PUBLIC_KEY = test_public_key
TEST_PRIVATE_KEY = test_private_key

with open(join(KEY_PATH, TEST_KEY, PUBLIC_KEY_TEMPLATE.format(TEST_SYSTEM_KEY)), 'r') as public_key_file:
  test_system_public_key = public_key_file.read()

with open(join(KEY_PATH, TEST_KEY, PRIVATE_KEY_TEMPLATE.format(TEST_SYSTEM_KEY)), 'r') as private_key_file:
  test_system_private_key = private_key_file.read()

TEST_SYSTEM_PUBLIC_KEY = test_system_public_key
TEST_SYSTEM_PRIVATE_KEY = test_system_private_key

SECRET_KEY = 'p%1xdl29wd5k=(%g$4h18$-7xroe-4s944(nf=by!(5i8p8vmf'

ALLOWED_HOSTS = (
  '*',
)

DEFAULT_APPS = (
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
  'django_nose',
)
LOCAL_APPS = (
  'apps.base',
  'apps.subscription',
  'apps.transactino',
)
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'woot.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
      join(WOOT_PATH, 'templates'),
    ],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

WSGI_APPLICATION = 'woot.wsgi.application'

DATABASES = {}

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

FILE_UPLOAD_HANDLERS = (
  'django.core.files.uploadhandler.MemoryFileUploadHandler',
  'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse'
    }
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
  },
  'loggers': {
    'django.request': {
      'handlers': ['mail_admins', 'console'],
      'level': 'ERROR',
      'propagate': True,
    },
  }
}

SCHEDULER = None
