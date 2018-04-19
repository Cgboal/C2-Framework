import docker
from ..db.SQLite import Helper


class ContainerMGMT:
    def __init__(self):
        self.client = docker.from_env()
        self.containers = self.client.containers.list()

    def run(self, image, module_id, command=None, **kwargs):
        db = Helper()

        if db.get_config('ssl') == "True":
            c2_url = "https://%s:%s" % (db.get_config('c2_host'), db.get_config('c2_port'))
        else:
            c2_url = "http://%s:%s" % (db.get_config('c2_host'), db.get_config('c2_port'))

        kwargs['environment'] = {
            "C2_URL": c2_url,
            "AGENT_ID": db.get_config("uuid"),
            "MODULE_ID": module_id
        }

        # Set name of container so it can be stopped later for updates,
        kwargs['name'] = module_id
        kwargs['auto_remove'] = True
        kwargs['detach'] = False
        print self.client.containers.run(image, command, **kwargs)

    def pull(self, name):
        if ":" in name:
            name, tag = name.split(":")
        else:
            tag = None
        try:
            self.client.images.pull(name, tag)
        except Exception:
            return False
        else:
            return True

