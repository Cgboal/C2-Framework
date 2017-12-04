# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Agent, Command, Agent_Group, Agent_Command_History
from api.serializers import UserSerializer, GroupSerializer, AgentSerializer, CommandSerializer, AgentCommandHistory
from django.shortcuts import render
from uuid import uuid4

# Create your views here.


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

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
        serializer = CommandSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, uuid=None):
        groups = Agent_Group.objects.filter(agent_id=uuid)
        commands_raw = Command.objects.filter(group_id__in=groups.group_id)
        commands_raw += Command.objects.filter(group_id=None)
        command_history = Agent_Command_History.objects.filter(agent_id=uuid)
        commands = commands_raw.exclude(id__in=command_history.id)
        serializer = CommandSerializer(commands, many=True)
        return Response(serializer.data)


class AgentCommandHistoryViewSet(viewsets.ViewSet):

    def create(self, request, uuid=None, command_id=None):
        command = Agent_Command_History(agent_id=uuid, command_id=command_id)
        command.save()
        serializer = AgentCommandHistory(command)
        return Response(serializer.data)
