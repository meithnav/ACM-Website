from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.events, name="events"),
    path("<event_name>", views.event_detail, name="event_detail"),
]
