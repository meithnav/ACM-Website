from django.contrib import admin
from .models import Event, Photo

admin.site.register((Event, Photo))
