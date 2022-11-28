from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.forecast, name="forecast"),
    path('forecast/', views.forecast, name="forecast"),
    path('archive/', views.archive, name="archive"),
    path('feedback/', views.feedback, name="feedback"),
    path('feedback_sent/', views.feedback_sent, name="feedback_sent"),
    path('about/', views.about, name="about"),
]