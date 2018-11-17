
from datetime import timedelta

from django.views import View
from django.http import JsonResponse
from django.utils import timezone

from apps.subscription.models import Account

class TransactinoTestView(View):
  def get(self, request, *args, **kwargs):

    account, account_created = Account.objects.get_or_create(public_key='test', is_verified=True, active_channel='no_channel')

    responses = {}
    for i in range(10):
      report, report_created = account.fee_reports.get_or_create(is_active=True, blocks_to_include=i+1)
      responses.update({
        i: report._id,
      })

    return JsonResponse(responses)
