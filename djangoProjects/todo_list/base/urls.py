from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, CustomLogoutView, RegisterPage
from todo_list.views import ToDoItemView

urlpatterns=[ 
    # to define a URL pattern for the custom register view 
    path('register/', RegisterPage.as_view(), name='register'),
    # to define a URL pattern for the custom login view 
    path('login/', CustomLoginView.as_view(), name='login'),
    # to define a URL pattern for the logout view 
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # This is for default page, that includes the tasks 
    # this is viewed when the request is received 
    path('', TaskList.as_view(), name='tasks'),  
    # this code snippet is used for when any task from the list is viewed in detail 
    # the path url is refreshed as '/task/<int:pk>/' 
    # task details are viewed as 'TaskDetail.as_view()' when any task from the task list is viewed
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),  
    path('task-create/', TaskCreate.as_view(), name='task-create'),  
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    # when path is directed to 'task-delete/<int:pk>/', DeleteView.as_view() is run, 
    # name represents that the name of the current view 
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),    
    path('todo_items/', ToDoItemView.as_view(),name= 'todo-items' ), # new URL 
    # URL for handling GET(retrieve), PUT(update), DELETE for a single item by primary key
    path('todo_items/<int:pk>/', ToDoItemView.as_view(), name='todo-item-detail')
    # <int:pk> : Django will expect an integer as part of the URL pass that value to the view as pk
]   