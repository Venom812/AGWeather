from django.http import HttpResponse
from .models import ForecastsRecord, ArchiveRecord
from .forecasts_scraper import scrap_forecasts

def forecasts(request):
    a = str(ForecastsRecord.objects.latest('rec_date').rec_data)
    b = str(ForecastsRecord.objects.latest('rec_date').rec_date)
    return HttpResponse(f"Hello, world. You're at the FORECASTS.____{a}___{b}")

def archive(request):
    x = str(ArchiveRecord.objects.latest('rec_date').rec_data)
    y = str(ArchiveRecord.objects.latest('rec_date').rec_date)
    return HttpResponse(f"Hello, world. You're in the ARCHIVE.____{x}___{y}")

def scrap_data(request):
    scrap_forecasts()
    return HttpResponse("OK")