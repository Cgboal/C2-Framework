# -*- coding: utf-8 -*-s
from __future__ import unicode_literals
import api.modules
from django.db import models
from uuid import uuid4
from api.helpers import import_modules, get_module_models


# Dynamically import all modules, and get a dictionary of the models used by modules
modules = import_modules(api.modules)
module_models = get_module_models(modules)

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


class Module(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=64)
    image = models.TextField(max_length=256, unique=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ":" + str(self.uuid)


class Module_Table(models.Model):
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    table_name = models.TextField()


class Agent_Module(models.Model):
    agent_id = models.ForeignKey(Agent, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)


class Group_Module(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)


class Log(models.Model):
    message = models.TextField()
    type = models.TextField(max_length=5)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

