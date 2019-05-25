
import json
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings

from apps.subscription.models import Address

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    address_value = '16FzUdcw2HVnwXhT73ZbRm57ZqELSTyz2v'
    address = Address.objects.create(value=address_value)
