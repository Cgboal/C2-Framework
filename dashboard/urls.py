from django.conf.urls import url, include
from dashboard.views import IndexView, LoginView, command_view, GroupCreateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^login/', LoginView.as_view()),
    url(r'^command/', command_view),
    url(r'^group/create', login_required(GroupCreateView.as_view()))
]