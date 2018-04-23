from django.db import models


class ModelTemplate(models.Model):
    agent_id = models.ForeignKey('api.Agent', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "api"
        abstract = True


class Descriptor(object):
    args = {}
