
import json
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.subscription.models import Account

from ...models import FeeReport

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    a, created = Account.objects.get_or_create()
    report = a.fee_reports.create(is_active=True, blocks_to_include=1)
