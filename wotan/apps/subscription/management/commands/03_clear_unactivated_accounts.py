
import json
import time
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ...models import Account

ten_minutes = timedelta(minutes=10)

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    while True:
      accounts_removed = []

      # 1. loop through activated subscriptions
      for account in Account.objects.filter(is_verified=False, is_superadmin=False):
        if timezone.now() - account.date_created > ten_minutes:
          accounts_removed.append(account._id)
          account.delete()

        # 2. print out updates
        if accounts_removed:
          print(json.dumps(accounts_removed, indent=2))

      # 3. sleep
      print('Waiting...')
      time.sleep(10)
