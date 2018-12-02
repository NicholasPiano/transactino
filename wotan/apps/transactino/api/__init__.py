
import json
import uuid

from django.middleware.csrf import get_token
from django.views import View
from django.http import JsonResponse

from util.get_ip import get_ip

from .schema import ProxySchema
from .schema.constants import proxy_constants

class ProxyView(View):
  def post(self, request):
    payload = {
      proxy_constants.ID: uuid.uuid4().hex,
      proxy_constants.IP: get_ip(request),
      proxy_constants.CHANNEL: uuid.uuid4().hex,
      proxy_constants.TRANSACTINO: json.loads(request.body.decode('utf-8'))
    }

    response = ProxySchema().respond(payload=payload).get_child(proxy_constants.TRANSACTINO)
    return JsonResponse(response.render())

  def get(self, request):
    return JsonResponse({
      'token': get_token(request),
    })
