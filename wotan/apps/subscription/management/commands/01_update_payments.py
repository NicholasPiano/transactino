
import json
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.bitcoin.models import Delta

from ...models import Payment, Address

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    while True:
      payments_confirmed = {}

      # 1. get active address
      active_address = Address.objects.get_active_address()

      # 2. loop through active payments
      if active_address is not None:
        for payment in Payment.objects.filter(is_open=True):
          btc_amount = payment.full_btc_amount / 10**8

          delta = Delta.objects.get(
            value=btc_amount,
            addresses__value=active_address.value,
            date_created__gt=payment.date_created,
          )

          if delta is not None:
            payment.is_open = False
            payment.time_confirmed = timezone.now()
            payment.block_hash = delta.to_transaction.block.hash
            payment.tx_hash = delta.to_transaction.hash
            payment.save()

            payments_confirmed.update({
              payment._id: {
                'tx_hash': payment.tx_hash,
                'time_confirmed': str(payment.time_confirmed),
              },
            })

        # 3. print out confirmations
        if payments_confirmed:
          print(json.dumps(payments_confirmed, indent=2))

      # 4. sleep
      print('Waiting...')
      time.sleep(10)
