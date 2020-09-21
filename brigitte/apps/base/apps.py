
from django.apps import AppConfig

from .constants import APP_LABEL

class BaseConfig(AppConfig):
  name = APP_LABEL
