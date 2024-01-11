"""
URL configuration for helpers_hub project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls), path("hub/", include("hub.urls"))]
