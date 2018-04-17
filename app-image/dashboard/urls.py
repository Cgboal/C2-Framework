from django.urls import path
from dashboard.views import IndexView, LoginView, command_view, GroupCreateView, logout_view, GroupView, \
    ModuleCreateView, ModuleView, RunView, AgentView, ReportView

from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', IndexView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout_view),
    path('command/', command_view),
    path('group/create/', login_required(GroupCreateView.as_view())),
    path('group/<int:group_id>/', login_required(GroupView.as_view())),
    path('module/add/', login_required(ModuleCreateView.as_view())),
    path('module/<uuid:module_id>/', login_required(ModuleView.as_view())),
    path('run/<int:group_id>/', login_required(RunView.as_view())),
    path('agent/<uuid:agent_id>/', login_required(AgentView.as_view())),
    path('report/<string:report_type>/<int:group_id>/', login_required(ReportView.as_view())),
    path('report/<string:report_type>/<uuid:entity_uuid>/', login_required(ReportView.as_view())),

]
