from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
import time

@shared_task(name = "scrap_data")
def scrap_data():
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
#   time.sleep(10)
  print(f"Current Time is {current_time}")


