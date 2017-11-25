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

class Group(models.Model):
    name = models.TextField(max_length=128)


class Agent_Group(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    agent_id = models.ForeignKey(Agent, on_delete=models.CASCADE)

class Command(models.Model):
    cmd = models.TextField(max_length=256)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)