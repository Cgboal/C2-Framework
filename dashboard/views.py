# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from api.models import Group, Command, Agent_Command_History, Agent_Group, Agent, Module
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
            for agent in agents:
                agent = Agent.objects.get(uuid=agent)
                agent_group = Agent_Group(agent_id=agent, group_id=group)
                agent_group.save()
        return render(request, template_name='index.html', context=context)

class GroupView(View):

    def get(self, request, group_id=None):
        context = get_nav_context(request)
        group = Group.objects.get(id=group_id)
        context['group'] = group
        agents_group = Agent.objects.filter(agent_group__group_id=group)
        context['agents_group'] = agents_group
        return render(request, template_name='group.html', context=context)

@login_required
def command_view(request):
    groups = Group.objects.all()
    context = {'groups': groups, 'status': ""}
    if request.method == "POST":
        cmd = Command(cmd=request.POST.get('cmd'), group_id=request.POST.get('group'))
        cmd.save()
        context['status'] = "Command added"
    return render(request, template_name='tmpInterface.html', context=context)