
import json
import subprocess
import datetime
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from util.bitcoin import get_block, get_info

from ...constants import bitcoin_constants
from ...models import Block

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    '''
    The purpose of this script is to extract only enough data from each block
    to allow the calculation of every transaction it contains. This involves
    looking back at individual transactions from previous blocks, but not extracting
    all data for the previous block.

    This script will proceed from the current block and wait until new data is available.
    It's primary aim is to make data available to the API as soon as possible.
    '''

    active_block_hash = get_info().get('bestblockhash')
    while True:
      # 1. wait for block hash
      while Block.objects.get(hash=active_block_hash, is_complete=True) is not None:
        active_block_hash = get_info().get('bestblockhash')
        print('Waiting...')
        time.sleep(60)

      # 2. process block
      start_time = timezone.now()
      active_block = Block.objects.create_from_hash(active_block_hash)
      processing_time = timezone.now() - start_time

      # 4. print out details
      print(json.dumps({
        'active_block_hash': active_block.hash,
        'active_block_height': active_block.height,
        'processing_time': str(processing_time),
        'number_of_transactions': active_block.transactions.count(),
      }, indent=2))
