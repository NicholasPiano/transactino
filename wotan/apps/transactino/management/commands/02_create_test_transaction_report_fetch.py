
import json

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings

from util.blockchaininfo import Block

from apps.transactino.models import TransactionReport

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    block = Block('0000000000000000000218ee3e7ed66c0c4344cd03b97dfac84c5546f66e7b88')
    if block.has_failed:
      return

    transaction_reports = TransactionReport.objects.filter(is_active=True)

    for transaction_report in transaction_reports:
      transaction_report.process(block)
