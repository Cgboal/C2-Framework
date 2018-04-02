from django.db import models
from api.models import Agent


class test:
    pass

class NmapResult(models.Model):
    host = models.TextField()
    open_ports = models.TextField()
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
