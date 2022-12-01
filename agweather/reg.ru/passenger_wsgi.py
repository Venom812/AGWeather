# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1854933/data/www/agweather.online/agweather')
sys.path.insert(1, '/var/www/u1854933/data/djangoenv/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'agweather.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

