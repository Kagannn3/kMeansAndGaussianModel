from django.contrib import admin
from .models import Task 

# Register your models here.
# to register a task model with the admin site 
# this allows the model to be viewed, edited and managed through the Django admin inerface 
admin.site.register(Task)
