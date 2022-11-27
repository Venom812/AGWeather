from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.forecast, name="forecast"),
    path('forecast/', views.forecast, name="forecast"),
    path('archive/', views.archive, name="archive"),
    path('feedback/', views.feedback, name="feedback"),
    path('about/', views.about, name="about"),
]