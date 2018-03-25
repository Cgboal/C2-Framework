import inspect, sys
from .lib.containers import ContainerMGMT
from rest import Rester


containers = ContainerMGMT()
rest = Rester()


def pull(cmd, *args, **kwargs):
    if not containers.pull(cmd[1]):
        rest.log_error("Failed to pull image %s" % cmd[1])
    rest.log_event("Image %s pulled" % cmd[1])


def run(cmd, *args, **kwargs):
    print "run 123"


def stop(cmd, *args, **kwargs):
    print "stop"


verbs = {name: obj for (name, obj) in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj))}