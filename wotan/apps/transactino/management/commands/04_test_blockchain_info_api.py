
import json

from django.core.management.base import BaseCommand, CommandError

from util.blockchaininfo import get_latest_block_hash, Block

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    latest_block_hash = get_latest_block_hash()

    block = Block(latest_block_hash)

    fees = []
    densities = []
    for transaction in block.transactions:
      fee, density = transaction.get_fee()
      fees.append(fee)
      densities.append(density)

    print(sum(fees) / len(fees))
    print(sum(densities) / len(densities))
