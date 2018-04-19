# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *
from api.serializers import UserSerializer, GroupSerializer, AgentSerializer, CommandSerializer, AgentCommandHistory,\
    Group, LogSerializer
from uuid import uuid4

# Create your views here.

class AgentViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Agent.objects.all()
        serializer = AgentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Agent.objects.all()
        agent = get_object_or_404(queryset, pk=pk)
        serializer = AgentSerializer(agent)
        return Response(serializer.data)

    def create(self, request):
        uuid = uuid4()
        if request.POST.get('uuid'):
            uuid = request.POST.get('uuid')
        agent, created = Agent.objects.get_or_create(uuid=uuid, name=request.POST.get('name'), os=request.POST.get('os'))
        agent.save()
        serializer = AgentSerializer(agent)
        return Response(serializer.data)


class CommandViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Command.objects.all()
        serializer = CommandSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        groups = Agent_Group.objects.filter(agent_id=pk).values_list('group_id', flat=True)
        commands_group = Command.objects.filter(group_id__in=groups)
        commands_all_agents = Command.objects.filter(group_id=None)
        commands_raw = commands_group | commands_all_agents
        command_history = Agent_Command_History.objects.filter(agent_id=pk).values_list('command_id', flat=True)
        commands = commands_raw.exclude(id__in=command_history)
        serializer = CommandSerializer(commands, context={'request': request}, many=True)
        return Response(serializer.data)


class AgentCommandHistoryViewSet(viewsets.ViewSet):

    def create(self, request):
        agent = Agent.objects.get(uuid=request.POST.get('uuid'))
        command = Command.objects.get(id=request.POST.get('command_id'))
        command_done = Agent_Command_History(agent_id=agent, command_id=command)
        command_done.save()
        serializer = AgentCommandHistory(command_done, context={'request': request})
        return Response(serializer.data)


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group, context={'request': request})
        return Response(serializer.data)


class LogViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Log.objects.all()
        serializer = LogSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        agent = Agent.objects.get(uuid=request.POST.get('uuid'))
        message = request.POST.get('message')
        type = request.POST.get('type')
        new_log = Log(message=message, type=type, agent=agent)
        new_log.save()
        serializer = LogSerializer(new_log, context={'request': request})
        return Response(serializer.data)


class ReportViewSet(viewsets.ViewSet):

    def create(self, request):
        post_data = json.loads(request.body.decode('utf-8'))
        module_id = post_data['module_id']
        agent_id = post_data['agent_id']

        module = Module.objects.get(uuid=module_id)
        agent = Agent.objects.get(uuid=agent_id)

        # TODO Re-enable this
        """
        try:
            agent_module = Agent_Module.objects.get(agent_id=agent, module_id=module)
        except ObjectDoesNotExist:
            return HttpResponseForbidden()
        """
        post_data['data']['agent_id'] = agent
        new_entry = module_models[post_data['table']](**post_data['data'])
        new_entry.save()
        return HttpResponse(status=200)

    # TODO add update method
    # def update(self, request, pk=None):
    #   pass
