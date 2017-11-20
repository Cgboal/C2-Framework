# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Agent
from api.serializers import UserSerializer, GroupSerializer, AgentSerializer
from django.shortcuts import render

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
        agent = Agent(name=request.data['name'], os=request.data['os'])
        agent.save()
        serializer = AgentSerializer(agent)
        return Response(serializer.data)

