from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.blog, name="blog"),
    path("<blog_name>", views.blog_detail, name="blog_detail"),
]
