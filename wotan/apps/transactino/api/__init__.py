
import json

from django.views import View
from django.http import JsonResponse

from .schema import ProxySchema

def ProxyView(View):
  def post(self, request):
    response = ProxySchema().respond(payload=json.loads(request.body)).render()
    return JsonResponse(response)
