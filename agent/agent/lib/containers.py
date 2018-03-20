import docker


class ContainerMGMT:
    def __init__(self):
        self.client = docker.from_env()
        self.containers = self.client.containers.list()

    def run(self, name, args, command=None):
        args['detatch'] = True
        self.client.containers.run(name, command, args)

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

