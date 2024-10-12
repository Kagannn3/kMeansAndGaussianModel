from pyexpat.errors import messages
from django.shortcuts import redirect, render
from rest_framework.response import Response
# (prediction) APIView represents the program which is in the server
# user (via web browser) try to access this program in the API
from rest_framework.views import APIView
from base.models import Tag, Task
from rest_framework import status 

from .permissions import Is_owner

from django_filters.rest_framework import DjangoFilterBackend 
# (prediction) the generics can be all types of API requests 
from rest_framework import generics 
from base.models import Task
# to convert json format 
from .serializers import TaskSerializer

# responsible for per-view schema generation 
from rest_framework.schemas import AutoSchema 
# 'include_docs_urls' is a function that generates URLs for API documentation 
# this allows documentation for your API endpoints 
from rest_framework.documentation import include_docs_urls

# coreapi is a python package that provides a set of tools for building APIs to generate API documentation 
# this is a class in coreapi that represents a single field in an API request or response 
# it is used to define the structure of API data, such as the type of data, its format, and any validation rules 
from coreapi import Field 
# Object is a class that represents a complex data structure, such as JSON object 
# used to define the structure of API data such as the fields and their types 
from coreschema import Object

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q


class ToDoItemView(APIView):
    # this code snippet is used for creating input placeholders for POST and PUT requests
    # openapi.Schema is the class for structure of the API documentation
    # openapi.TYPE_BOOLEAN is used to determine the boolean placeholder for the API documentation
    # this code snippet is used for editing and creating the API documentation


    @login_required
    def task_list(request):
        # Each users should login to access their tasks
        tasks = Task.objects.filter(user=request.user).order_by('priority')
        tasksUpcoming = tasks.filter(due_date__lte=datetime.today() + datetime.timedelta(days=7)) # for next tasks 
        search_query = request.GET.get('search')
        if search_query:
            tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        tags = Tag.objects.all()
        return render(request, 'task_list.html', {'tasks': tasks, 'next_tasks': tasksUpcoming, 'tags': tags})


    def task_detail(request, pk):
        task = Task.objects.get(pk=pk)
        comments = task.comments.all()
        attachments = task.attachments.all()

        return render(request, 'task_detail.html', {'task': task, 'comments': comments, 'attachments': attachments})

    def task_update(request, pk):
        task = Task.objects.get(pk=pk)
        # Send notification to assigned user
        messages.success(request, 'Task updated!')
        return redirect('task_detail', pk=pk)

    # the list of the all tasks
    queryset=Task.objects.all()
    # DjangoFilterBackend allows to filter queryset results by specific fields through query parameters in the URL
    filter_backends=[DjangoFilterBackend]
    # filter tasks by their completion status 
    # to filter completed tasks: "GET/todo_items/?completed=true"
    # to filter incompleted tasks: "GET/todo_items/?completed=false"
    setOf_filter_fields= ['completed']
    # list of permission class 
    # these classes determine whether a request should be granted or denied access to specific action 
    # The permission_class in Django Rest Framework allows you to control who has access to certain API views or actions
    # to able to edit or delete the specific object, requested user should valid the requirements in the permission_classes
    permission_classes=[Is_owner] # this is only allow the owner of the task to edit or delete it 
    # self represents the APIView class
    serializer_class=TaskSerializer  # get a single todo item (by primary key) 
    # when ToDoItemView.as_view() function is run, firstly, this get function will be run due to the APIView default class
    def get(self, request, pk=None): 
        if pk: # if pk is not None
            try: 
                # pk is the primary key (id number of the task)
                todo_item=Task.objects.get(pk=pk)
            except Task.DoesNotExist: # there is no task object 
                return Response({"error": "Todo item not found"}, status=status.HTTP_404_NOT_FOUND)
            # to convert json format 
            serializer=TaskSerializer(todo_item) 
            return Response(serializer.data)
        else: # if no pk is provided, return all todo items 
            todo_items=Task.objects.all()
            serializer=TaskSerializer(todo_items,many=True)
            return Response(serializer.data)
        
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                #these are the parameters of the POST request
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the todo item'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description= 'The details about the task'),
                'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the todo item is completed'),
            },
            required=['title'],

        ),

        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT, # type is the argument to send to the server 
                # openapi represents to the API documentation 
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the todo item'),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the todo item'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description= 'The details about the task'),
                    'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the todo item is completed'),
                },
            ),
        },
    )


    # self represents the APIView class 
    def post(self, request):

        serializer=TaskSerializer(data=request.data)
        # to create a new todo item
        # request.data['title'] is title data of the requested post
        # which is assigned to the title variable in the database 
        # posted task's title 
        if serializer.is_valid():
        # Model class from the 'models' module has a save() function to save Model(todo_item in this case) to the database
        # save the todo item to the database
            serializer.save()
        # to reply successfully of the post request 
            # presents the new posted task's data and the successful message (HTTP 201 created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # to reply failed of the post request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type= openapi.TYPE_OBJECT,
            properties={
                # openapi.Schema represents the complex object in the API document 
                'title': openapi.Schema(type=openapi.TYPE_STRING, description= 'Title of the item'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description= 'The details about the task'),
                'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description= 'Whether the todo item is completed'),
            },
            required=['title'],
        ),
        
        consumes=['application/json'], # this is the the format type of the used input requests(json format)
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT, 
                properties={ # openapi is a module that includes some pre-created structures for the API documentation 
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description= 'ID of the todo item'),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, description= 'The title of the task'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description= 'The details about the task'),
                    'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description= 'Whether the task is completed'),
                },
            ),
        },
    )

    def put(self, request, pk):
        try:
            todo_item=Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task with could not be found"}, status=status.HTTP_404_NOT_FOUND)

        # to check the requested user has permission to put method on this todo item 
        self.check_object_permissions(request, todo_item)
        # serialized of the requested data 
        # this below code line requested data applied on the todo_item(already exist task)
        # this serializer variable represents the updated data on the task 
        serializer=TaskSerializer(todo_item, data=request.data) 
        # todo_item is assigned to the specific task object which is selected for updating 
        # to update a todo item
        # the task whose id is 'pk', is assigned to the todo_item variable 
        if serializer.is_valid(): 
            # saved updated task to the database 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: # if todo item is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        # to delete a todo item 
        if pk: # if pk is not None 
            todo_item=Task.objects.get(pk=pk)
            # to check the requested user has permission to delete the task 
            self.check_object_permissions(request, todo_item)
            # delete the todo item from the database
            return Response({'message': 'Todo item is deleted successfully'})
        else: # if pk is None 
            return Response({"error": "There is not any selected todo item "})

# JWT (JSON Web Tokens) is a popular method to authenticate users in APIs  
     

    # self is an instance of the ToDoItemView class 
    # this method returns a schema object(document includes API responses) that describes the structure of the API request or response 
    def get_schema(self):
        # creating AutoSchema object, which is a class from Django Rest Framework that generates a schema for an API endpoint 
        # manual_fields is a list of Field object that define structure of the API request or response (for instance, places for the title, description, and complete in the form )
        
        # to create AutoSchema object
        # AutoSchema is a class from Django Rest Framework that generates a schema for an API endpoint 
        # manual_fields argument is a list of Field objects that define the structure of the API request or response 
        # in this situation, there is only 1 Field object in the list 
        schema=AutoSchema(manual_fields=[
            Field('body', location='body', schema=Object(title= 'Task data'))
        ])
        return schema
    
    # property is function for getting an attribute value of the get_schema method 
    schema=property(get_schema)


   


