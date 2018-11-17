
import json
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ...models import Subscription

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    while True:
      subscriptions_updated = {}

      # 1. loop through activated subscriptions
      for subscription in Subscription.objects.filter(has_been_activated=True):
        if subscription.activation_date > timezone.now():
          subscription.is_active = True
          subscription.save()

          subscriptions_updated.update({
            subscription._id: 'activated',
          })

        if subscription.valid_until < timezone.now():
          subscription.is_active = False
          subscription.save()

          subscriptions_updated.update({
            subscription._id: 'deactivated',
          })

        # 2. print out updates
        if subscriptions_updated:
          print(json.dumps(subscriptions_updated, indent=2))

      # 3. sleep
      print('Waiting...')
      time.sleep(10)
