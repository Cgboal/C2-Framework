from django.conf.urls import url, include
from dashboard.views import index_view, command_view, GroupCreateView


urlpatterns = [
    url(r'^$', index_view),
    url(r'^command/', command_view),
    url(r'^group/create', GroupCreateView.as_view())
]