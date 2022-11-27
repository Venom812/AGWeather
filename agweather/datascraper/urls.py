from django.urls import path

from . import views

urlpatterns = [
    path('', views.forecasts, name='forecasts'),
    path('archive/', views.archive, name='archive'),

]