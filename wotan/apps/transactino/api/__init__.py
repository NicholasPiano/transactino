
import json

from django.views import View
from django.http import JsonResponse

from apps.subscription.models import Connection

from .constants import api_constants, consumer_constants
from .schema import TransactinoSchema

def api(connection=None, payload=None):
  return TransactinoSchema().respond(connection=connection, payload=payload).render()
