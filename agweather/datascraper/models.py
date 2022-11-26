from django.db import models

# Create your models here.
class ForecastsRecord(models.Model):
    rec_date = models.DateTimeField()
    rec_data = models.JSONField()