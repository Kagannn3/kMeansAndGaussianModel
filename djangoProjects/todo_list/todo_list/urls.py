"""
URL configuration for todo_list project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# routers module provides a way to define API routes using Django Rest Framework
# permission module is used to control who can access the Swagger documentation 
from rest_framework import routers, permissions
# this function generates a schema view that serves the API documentation 
from drf_yasg.views import get_schema_view
# this is used to configure metadata about your API like the title, version and description 
from drf_yasg import openapi

#views module where we will define our API views
from . import views
# TokenObtainPairView class provides that each token of users with their corresponding authorization by view
# JWT tokens typically have a short lifespan for security reasons like 5-10 minutes 
# Once the access token expires, clients can no longer use it to authenticate requests
# instead of requiring the user to log in again, the TokenRefreshView allows the client to obtain a new access token using a refresh token 
# access token is a short-lived and used to authenticate API requests
# refresh token is longer-lived and can be used to get a new access token when the current one expires 

# when a user logs in, they gets boths an access token and refresh token 
# once the access token expires, the client sends the refresh token to the TokenRefreshView endpoint to get a new access token 

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# this line used for editing API documentation view(this is a documentation which clarifies the API features and how does this API system work?)
schema_view=get_schema_view(
    openapi.Info(
        title="Todo API", # title of the API documentation
        default_version= 'v1',  # API version
        description= "API documentation for the Todo app",  # description for the API 
    ),
    public=True,  
    permission_classes=[permissions.AllowAny], # to allow anyone to access the documentation
)


# to create a SimpleRouter instance and registering our ToDoItemView with the router 
# the basename parameter specifies the base name for the URL patterns
router=routers.SimpleRouter()
# is a simple router that provides a way to define API routes 
# when we register a viewset with the router, DRF automtically generates URL patterns for the viewset's actions (e.g. list, create, retrieve, update, destroy)
# the basename parameter helps DRF to generate unique URL names for each action 
# by including the router's URL patterns in our urlpatterns list, we are making our API routes avaliable to the Django project 
router.register(r'tasks', views.ToDoItemView, basename='tasks')

urlpatterns = [


    path('admin/', admin.site.urls),
    # include() function is used to include URL pattrns from other URLconfs
    # making it easy to modularize the URL 
    path('api/', include('base.urls')), # this include URLs of the app
    # this path is used to able to pull urls patterns which are in the database
    path('', include('base.urls')), 
    # the basename parameter helps DRF to generate unique URL namess for each action
    
    # when the user logs in, who will receieve a token in response 
    # and use this token in the Authorization header when making API requests
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # this view allows clients to refresh an expired access token using the refresh token 
    # if you have refresh token, you can send it to the 'api/token/refresh' endpoint to get a new access token 
    # this is beneficial because it avoids requiring the user to log in again after their access token has expired 
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  


] 
# redis, celery
# Redis is an in-memory data store that can be used as a database and message broker for Celery
# Redis is a NoSQL database that stores data in RAM, making it fast and efficient 
# Celery is a distributed task queue that allows to run tasks asynchronously in the background 

#Celery represents how a task queue works:
# a task is added to the queue
# the task is stored in the queue until a worker node is avaliable to execute it 
# a worker node becomes avaliable and takes the task from the queue 
# the worker node executes the task 
# the task is removed from the queue once it is executed 

