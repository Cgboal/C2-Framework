# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from api.models import Group, Command, Agent_Command_History, Agent_Group
# Create your views here.


def IndexView(request):
    return render(request, template_name='index.html')


def CommandView(request):
    groups = Group.objects.all()
    context = {'groups': groups, 'status': ""}
    if request.method == "POST":
        cmd = Command(cmd=request.POST.get('cmd'), group_id=request.POST.get('group'))
        cmd.save()
        context['status'] = "Command added"
    return render(request, template_name='tmpInterface.html', context=context)