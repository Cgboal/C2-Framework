from django.conf.urls import url, include
from django.contrib import admin
from stager.views import StagerView, LatestView
from dashboard.views import Index



urlpatterns = [
    url(r'^install', StagerView),
    url(r'^latest', LatestView),
]