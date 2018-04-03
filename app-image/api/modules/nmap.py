from django.db import models
from .lib.templates import ModelTemplate


class Descriptor(object):
    def __init__(self):
        self.name = "Nmap"
        self.image = "c2f-nmap:latest"


class NmapResult(ModelTemplate):
    host = models.TextField()
    open_ports = models.TextField()

