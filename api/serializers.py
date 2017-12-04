from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Agent, Command, Agent_Command_History


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class AgentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agent
        fields = ('uuid', 'name', 'os', 'installed_at', 'last_seen')


class CommandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Command
        fields = ('id', 'cmd', 'group_id')


class AgentCommandHistory(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agent_Command_History
        fields = ('id', 'command_id', 'completed')