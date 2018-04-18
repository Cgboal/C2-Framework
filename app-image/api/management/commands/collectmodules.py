import api.modules
import inspect
import json
from api.helpers import import_modules
from hashlib import sha256
from django.core.management.base import BaseCommand, CommandError
from api.models import Module, Module_Table
from api.lib.templates import ModelTemplate, Descriptor


class Command(BaseCommand):
    help = 'Creates DB entries for all installed C2F modules'

    def handle(self, *args, **options):
        module_list = import_modules(api.modules)
        for module in module_list:
            for member in module[1]:
                mname = member[0]
                if issubclass(member[1], Descriptor):
                    class_ = getattr(module[0], mname)
                    instance = class_()
                    module_args = {}
                    if instance.args:
                        module_args = instance.args
                    module_args = json.dumps(module_args)
                    m, output = Module.objects.get_or_create(image=instance.image, defaults={'name': instance.name, 'args': module_args})
                    print("Added module %s" % instance.name)
                elif issubclass(member[1], ModelTemplate):
                    module_table, output = Module_Table.objects.get_or_create(module_id=module, table_name=member[0])
                    module_table.save()

