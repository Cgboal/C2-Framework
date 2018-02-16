# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import Command, Group, Agent, Agent_Group

# Register your models here.
admin.site.register(Command)
admin.site.register(Group)
admin.site.register(Agent)
admin.site.register(Agent_Group)