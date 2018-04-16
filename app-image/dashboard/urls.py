from django.conf.urls import url, include
from django.urls import path
from dashboard.views import IndexView, LoginView, command_view, GroupCreateView, logout_view, GroupView, \
    ModuleCreateView, ModuleView, RunView, AgentView

from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', logout_view),
    url(r'^command/', command_view),
    url(r'^group/create', login_required(GroupCreateView.as_view())),
    url(r'^group/(?P<group_id>\w+)/$', login_required(GroupView.as_view())),
    url(r'^module/add', login_required(ModuleCreateView.as_view())),
    path(r'^module/<uuid:module_id>/$', login_required(ModuleView.as_view())),
    url(r'^run/(?P<group_id>\w+)/$', login_required(RunView.as_view())),
    path(r'^agent/<uuid:agent_id>/$', login_required(AgentView.as_view()))
]