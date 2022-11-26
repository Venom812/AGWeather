from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from .forecasts_scraper import scarp_forecasts
from .models import ForecastsRecord
from django.utils import timezone

@shared_task(name = "scrap_data")
def scrap_data():
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  print(f"Current Time is {current_time}")

  json_data = scarp_forecasts()

  ForecastsRecord.objects.create(rec_date=timezone.now(), rec_data=json_data)

