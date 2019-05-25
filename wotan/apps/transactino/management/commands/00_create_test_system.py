
import json
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings

from apps.subscription.models import System

class Command(BaseCommand):
  help = ''

  def handle(self, *args, **options):
    private_key = settings.TEST_PRIVATE_KEY
    public_key = settings.TEST_PUBLIC_KEY

    system = System.objects.create_and_import(
      private_key=private_key,
      public_key=public_key,
    )
