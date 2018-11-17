
import json
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.subscription.models import Account

from ...models import FeeReport

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    while True:
      # 1. loop through activated reports
      for report in FeeReport.objects.filter(is_active=True):
        report.process()
        print(report.average_tx_fee, report.average_tx_fee_density)

      # 3. sleep
      print('Waiting...')
      time.sleep(60)
