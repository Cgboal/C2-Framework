# -*- coding: utf-8 -*-s
from __future__ import unicode_literals

from django.db import models
from uuid import uuid4
# Create your models here.


class Agent(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=32)
    os = models.TextField(max_length=256)
    installed_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
