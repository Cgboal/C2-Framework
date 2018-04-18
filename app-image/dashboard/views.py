# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import api.modules
from django.conf import settings
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from api.helpers import *

from api.models import Group, Command, Agent_Command_History, Agent_Group, Agent, Module, Agent_Module, Group_Module, \
    Log, Module_Table

module_models = get_module_models(import_modules(api.modules))
# Create your views here.


def get_nav_context(request):
    agents = Agent.objects.all()
    groups = Group.objects.all()
    modules = Module.objects.all()
    username = request.user.username
    return {
        "agents": agents, "groups": groups, "modules": modules,
        "username": username
    }


class IndexView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        context = get_nav_context(request)
        return render(request, template_name='index.html', context=context)


class LoginView(View):

    def get(self, request):
        return render(request, template_name='login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, template_name='login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


class GroupCreateView(View):
    
    def get(self, request):
        context = get_nav_context(request)
        return render(request, template_name='group_create_form.html', context=context)

    def post(self, request):
        context = get_nav_context(request)
        name = request.POST.get('group-name')
        description = request.POST.get('description')
        agents = request.POST.getlist('agent')
        modules = request.POST.getlist('module')
        if name:
            group = Group(name=name)
            group.save()
            for module in modules:
                module = Module.objects.get(uuid=module)
                group_module = Group_Module(group_id=group, module_id=module)
                group_module.save()
                command_string = {
                    "action": "add",
                    "module": {
                        "uuid": str(module.uuid),
                        "name": module.name,
                        "image": module.image
                    }
                }
                new_command = Command(cmd=json.dumps(command_string), group_id=group)
                new_command.save()
            for agent in agents:
                agent = Agent.objects.get(uuid=agent)
                agent_group = Agent_Group(agent_id=agent, group_id=group)
                agent_group.save()

                for module in modules:
                    module = Module.objects.get(uuid=module)
                    agent_module, created = Agent_Module.objects.get_or_create(agent_id=agent, module_id=module)
                    agent_module.save()
                    
        return render(request, template_name='index.html', context=context)


class GroupView(View):

    def get(self, request, group_id=None):
        context = get_nav_context(request)
        group = Group.objects.get(id=group_id)
        context['group'] = group
        agents_group = Agent.objects.filter(agent_group__group_id=group)
        context['agents_group'] = agents_group
        group_modules = Module.objects.filter(group_module__group_id=group)
        context['group_modules'] = group_modules
        return render(request, template_name='group.html', context=context)


class ModuleCreateView(View):

    def get(self, request):
        context = get_nav_context(request)
        return render(request, template_name='module_upload.html', context=context)

    def post(self, request):
        if request.FILES:
            uploaded_file = request.FILES["file"]
            module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/api/modules/" + uploaded_file.name
            with open(module_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
                return HttpResponse("Module upload successful")
        elif request.POST.get("apply"):
            import subprocess
            restart = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/assimilate.sh"
            subprocess.call([restart])
            return redirect("/")


class ModuleView(View):

    def get(self, request, module_id=None):
        context = get_nav_context(request)
        module = Module.objects.get(uuid=module_id)
        context['module'] = module
        return render(request, template_name='module.html', context=context)


class RunView(View):
    
    def get(self, request, group_id=None):
        if not group_id:
            return HttpResponse(status=400)
        group = Group.objects.get(id=group_id)
        group_modules = Module.objects.filter(group_module__group_id=group)
        for module in group_modules:
            command_str = {
                "action": "run",
                "module": {
                    "uuid": str(module.uuid)
                },
                "args": json.loads(module.args)
            }
            command = Command(cmd=json.dumps(command_str), group_id=group)
            command.save()
        return redirect("/")


class AgentView(View):

    def get(self, request, agent_id=None):
        context = get_nav_context(request)
        agent = Agent.objects.get(uuid=agent_id)
        logs = Log.objects.filter(agent=agent)

        context["agent"] = agent
        context["logs"] = logs

        return render(request, template_name='agent.html', context=context)


class ReportView(View):

    def get(self, request, report_type=None, group_id=None, entity_uuid=None):
        context = get_nav_context(request)
        context["report_type"] = report_type.capitalize()
        if report_type == "group":
            group = Group.objects.get(id=group_id)
            agents = Agent.objects.filter(agent_group__group_id=group)
            modules = Module.objects.filter(group_module__group_id=group)

            context["outer"] = group
            context["inner"] = modules
            context["inner_type"] = "Modules"
            context["reports"] = {}

            for module in modules:
                context["reports"][module.name] = {}
                context["reports"][module.name]["name"] = module.name
                tables = Module_Table.objects.filter(module_id=module)
                for table in tables:
                    model = module_models[table.name]
                    context["reports"][module.name]["tables"] = {}
                    context["reports"][module.name]["tables"][table.name] = {}
                    context["reports"][module.name]["tables"][table.name]["name"] = table.name
                    context["reports"][module.name]["tables"][table.name]["columns"] = [f.name for f in model._meta.get_fields()]
                    context["reports"][module.name]["tables"][table.name]["entries"] = serializers.serialize("python", model.objects.filter(agent_id__in=agents))

        return render(request, template_name='report.html', context=context)



        """
        elif report_type == "agent":
            agent = Agent.objects.get(uuid=entity_uuid)1425786=
            groups = Group.objects.filter(agent_group__agent_id=agent)
            modules = Module.objects.filter(group_module__group_id__in=groups)=
            module = Module.objects.get(uuid=entity_uuid)
            groups = Group.objects.filter(group_module__module_id=module)
            agents = Agent.objects.filter(agent_group__group_id__in=groups)
            tables = Module_Table.objects.filter(module_id=module)

        context = {
            "outer": {
                "modules": modules
            },
            "inner": {
                "groups": groups,
                "agents": agents

            },
            "reports": {
                module.name: {
                    "table_name": [results]
                }
            }
        }
        """


@login_required
def command_view(request):
    groups = Group.objects.all()
    context = {'groups': groups, 'status': ""}
    if request.method == "POST":
        cmd = Command(cmd=request.POST.get('cmd'), group_id=request.POST.get('group'))
        cmd.save()
        context['status'] = "Command added"
    return render(request, template_name='tmpInterface.html', context=context)