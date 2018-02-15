from django.conf.urls import url, include
from dashboard.views import IndexView, CommandView


urlpatterns = [
    url(r'^$', IndexView),
    url(r'^command/', CommandView)
]