# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from api.models import Group, Command, Agent_Command_History, Agent_Group, Agent, Module, Agent_Module, Group_Module
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
        modules = request.POST.getlist('modules')
        if name:
            group = Group(name=name)
            group.save()
            for module in modules:
                group_module = Group_Module(group_id=group, module_id=module)
                group_module.save()
                command_string = "add %s %s %s" % (module.uuid, module.name, module.image)
                new_command = Command(cmd=command_string, group_id=group)
                new_command.save()
            for agent in agents:
                agent = Agent.objects.get(uuid=agent)
                agent_group = Agent_Group(agent_id=agent, group_id=group)
                agent_group.save()

                for module in modules:
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
        return render(request, template_name='module_upload.html')

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
            return render(request, template_name="index.html")


class ModuleView(View):

    def get(self, request, module_id=None):
        context = get_nav_context(request)
        module = Module.objects.get(uuid=module_id)
        context['module'] = module


@login_required
def command_view(request):
    groups = Group.objects.all()
    context = {'groups': groups, 'status': ""}
    if request.method == "POST":
        cmd = Command(cmd=request.POST.get('cmd'), group_id=request.POST.get('group'))
        cmd.save()
        context['status'] = "Command added"
    return render(request, template_name='tmpInterface.html', context=context)