"""Module fo periodic scraping data."""
from __future__ import absolute_import, unicode_literals
from datetime import datetime
from celery import shared_task
from django.utils import timezone
from .forecasts_scraper import scrap_forecasts
from .archive_scraper import scrap_archive
from .models import ForecastsRecord, ArchiveRecord


@shared_task(name="scrap_data")
def scrap_data():
    """Shared scraping task."""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Current Time is {current_time}")

    json_forecasts_data = scrap_forecasts("datascraper/datascraper_config.json")
    json_archive_data = scrap_archive("datascraper/datascraper_config.json")

    if json_forecasts_data:
        ForecastsRecord.objects.create(
            rec_date=timezone.now(), rec_data=json_forecasts_data)

    if json_archive_data:
        ArchiveRecord.objects.create(
            rec_date=timezone.now(), rec_data=json_archive_data)
