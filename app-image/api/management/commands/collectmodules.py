import api.modules
import inspect
from api.helpers import import_modules
from hashlib import sha256
from django.core.management.base import BaseCommand, CommandError
from api.models import Module


class Command(BaseCommand):
    help = 'Creates DB entries for all installed C2F modules'

    def handle(self, *args, **options):
        module_list = import_modules(api.modules)
        for module in module_list:
            for member in module[1]:
                mname = member[0]
                if mname == "Descriptor":
                    class_ = getattr(module[0], mname)
                    instance = class_()
                    m, output = Module.objects.get_or_create(name=instance.name, image=instance.image)
                    print("Added module %s" % instance.name)