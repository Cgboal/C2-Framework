from django.db import models
from api.lib.templates import ModelTemplate


class Descriptor(object):
    def __init__(self):
        self.name = "Hello-World"
        self.image = "cgboal/c2f-modules:HelloWorld"


class HelloWorldResult(ModelTemplate):
    random_string = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

