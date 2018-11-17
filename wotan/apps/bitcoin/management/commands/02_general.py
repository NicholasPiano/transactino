
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ...models import Block

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    block_hash = '000000000000000000185bb785a144202e9715007fc150a95cd464755f3a3562'
    raw_block = Block.objects.raw(block_hash)

    for raw_transaction in raw_block.raw_transactions:
      print(raw_transaction.get_fee())
