
import json

from django.middleware.csrf import get_token
from django.views import View
from django.http import JsonResponse

from .schema import ProxySchema

class ProxyView(View):
  def post(self, request):
    response = ProxySchema().respond(payload=json.loads(request.body)).render()
    return JsonResponse(response)

  def get(self, request):
    return JsonResponse({
      'token': get_token(request),
    })
