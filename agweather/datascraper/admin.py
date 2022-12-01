from django.contrib import admin

# Register your models here.
from .models import ForecastsRecord, ArchiveRecord

admin.site.register(ForecastsRecord)
admin.site.register(ArchiveRecord)