from django.db import models
from django.contrib.auth.models import User 

class Tag(models.Model):
    name = models.CharField(max_length=255)


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')

# Create your models here.
class Task(models.Model): # the data model of task database
    # this keeps the user strings in the database moodel
    # on_delete means that, 
    # what should happen to the user field when the referenced user instance is deleted 
    # models.CASCADE specifies that, 
    # when the referenced user is deleted, all related instances in this model also be deleted 
    # blank specifies that, the field is allowed to be empty in forms 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # the task name
    title = models.CharField(max_length=200)
    # the task description
    description = models.TextField(null=True, blank=True)
    # the task completion status 
    complete = models.BooleanField(default=False)
    # the timestap of when the task was created 
    created = models.DateTimeField(auto_now_add=True)
    
    priority = models.IntegerField(default=1)  # to sort from 1 to end
    due_date = models.DateField(null=True, blank=True)  # this is used to display tasks with their object to determine their upcoming date  
    tags = models.ManyToManyField('Tag')
    comments = models.ManyToManyField('Comment')
    attachments = models.ManyToManyField('Attachment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    # without a __str__ method, Django represent the object something like "<Task: Task object (1)>"
    # which is not very informative 
    # In Django admin interface, will show the string returned by __str__, 
    # this is making easier to understand records 
    def __str__(self):
        return self.title 
    
    # to establish a default order for querysets, ensuring consistent and efficient data retrieval
    class Meta:
        ordering = ['complete']

