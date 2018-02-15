import docker


class ContainerMGMT():
    def __init__(self):
        self.client = docker.from_env()
