from django.db.models import Model
#Defining a module descriptor
class Module():
    def __init(self):
        self.name = "Example Name"
        self.container = "Container Name"
        self.options = {
            "example_option": "default value"
        }

#All classes not named Module will be considered to be Models
class table_1(Model):
    pass