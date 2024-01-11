from django.urls import path

from . import views

urlpatterns = [path("master/", views.maser_bot, name="master_bot")]
