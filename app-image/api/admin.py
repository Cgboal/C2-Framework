# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import api.modules
from django.contrib import admin
from api.models import Command, Group, Agent, Agent_Group, Module, Agent_Module
from api.helpers import get_module_models, import_modules
# Register your models here.
admin.site.register(Command)
admin.site.register(Group)
admin.site.register(Agent)
admin.site.register(Agent_Group)
admin.site.register(Module)
admin.site.register(Agent_Module)
for name, model in get_module_models(import_modules(api.modules)).items():
    admin.site.register(model)
