from django.http import HttpResponse
from .models import ForecastsRecord

a = ForecastsRecord.objects.latest('rec_date').rec_date

print(a)

def index(request):
    return HttpResponse("Hello, world. You're at the datascraper index." + str(a))