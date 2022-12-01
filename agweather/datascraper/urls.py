from django.urls import path

from . import views

urlpatterns = [
    path('', views.forecasts, name='forecasts'),
    path('ar/', views.archive, name='archive'),
]