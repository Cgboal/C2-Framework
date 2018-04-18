from django.db import models
from api.lib.templates import ModelTemplate, Descriptor


class HelloWorld(Descriptor):
    name = "Hello-World"
    image = "cgboal/c2f-modules:HelloWorld"


class HelloWorldResult(ModelTemplate):
    random_string = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

