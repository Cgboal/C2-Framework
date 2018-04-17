import inspect, sys
from .lib.containers import ContainerMGMT
from .db.SQLite import Helper
from rest import Rester


def add(cmd, *args, **kwargs):
    containers = ContainerMGMT()
    rest = Rester()
    db = Helper()

    uuid, name, image = cmd[1:4]

    db.create_module(uuid, name, image)

    if not containers.pull(image):
        rest.log_error("Failed to pull image: %s" % image)
    rest.log_event("Image pulled: %s" % image)
    rest.log_event("Module added: %s" % name)


def run(cmd, *args, **kwargs):
    containers = ContainerMGMT()
    rest = Rester()
    db = Helper()

    uuid = cmd[1]

    module = db.get_module(uuid)

    containers.run(module.image, module.uuid)
    rest.log_action("Module executed: %s" % module.name)

def stop(cmd, *args, **kwargs):
    print "stop"


verbs = {name: obj for (name, obj) in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj))}