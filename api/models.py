# -*- coding: utf-8 -*-s
from __future__ import unicode_literals

from django.db import models
from uuid import uuid4
# Create your models here.


class Agent(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=32)
    os = models.TextField(max_length=256)
    installed_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.TextField(max_length=128)

    def __str__(self):
        return self.name


class Agent_Group(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    agent_id = models.ForeignKey(Agent, on_delete=models.CASCADE)


class Command(models.Model):
    cmd = models.TextField(max_length=256)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.cmd


class Agent_Command_History(models.Model):
    agent_id = models.ForeignKey(Agent, on_delete=models.CASCADE)
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE)
    completed = models.BooleanField(default=True)