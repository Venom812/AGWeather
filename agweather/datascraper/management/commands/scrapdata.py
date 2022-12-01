"""Django-admin command to scrap data."""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datascraper.models import ForecastsRecord, ArchiveRecord
from datascraper.forecasts_scraper import scrap_forecasts
from datascraper.archive_scraper import scrap_archive


class Command(BaseCommand):
    """Django command."""
    help = 'Scraps forecasts and weather archive data to database'

    def handle(self, *args, **kwargs):

        json_forecasts_data = scrap_forecasts("datascraper/datascraper_config.json")
        if json_forecasts_data:
            ForecastsRecord.objects.create(
                rec_date=timezone.now(), rec_data=json_forecasts_data)
            self.stdout.write(timezone.now().isoformat() +
                " Forecasts data successfully scraped to database.")

        json_archive_data = scrap_archive("datascraper/datascraper_config.json")
        if json_archive_data:
            ArchiveRecord.objects.create(
                rec_date=timezone.now(), rec_data=json_archive_data)
            self.stdout.write(timezone.now().isoformat() +
                " Weather archive data successfully scraped to database.")
