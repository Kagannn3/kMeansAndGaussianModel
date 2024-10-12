from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import LoginRequiredMixin  # when you entered the browser, you firstly must to login with your credentials 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect 
from .models import Task 
# Create your views here.

# REST(Representational State of Resource) is an architectural style for designing networked applications
# it is based on the idea of resources, which aare iddentiffied by URIs(Uniform Resource Identifiers), 
# and can be manipulated using a fixed set of operations 
# REST API is a way for different systems to comunicate with each other over the internet 
# it allows different applications to exchange data in a structured way
# the server does not have any information about the client between requests
# responses from the server can be cached by the client 
# a uniform interface is used to communicate between client and server, including HTTP methods(e.g. GET,POST,PUT,DELETE) and standard HTTP status code 
# there is a layered system, each layer are responsible for a specific function (e.g. authentication, encryption)

# the most common HTTP methods used in REST APIs:
# GET(receive a resource), POST(create a new resource), PUT(update an existing resource) and DELETE(delete a resource)
class CustomLoginView(LoginView): # this is a subclass of Django's built-in 'LoginView'
    template_name= 'base/login.html'
    fields='__all__' # all fields of the login.html
    # to redirect authenticated users to the 'tasks' URL 
    redirect_authenticated_user= True

    # override the default success URL to redirect to the 'tasks' URL after login 
    def get_success_url(self): 
        # return the 'tasks' URL as the success URL 
        return reverse_lazy('tasks')

# FormView is a pre-prepared class for register page 
# it provides to prepare the register page easily and quickly 
class RegisterPage(FormView): 
    # template_name attribute represents the file to be run for the register page 
    template_name= 'base/register.html'
    # this line determines the form type to the register page 
    form_class=UserCreationForm
    # after the registeration successfully, it will redirect to the authenticated user to the tasks component 
    redirect_authenticated_user= True
    success_url=reverse_lazy('tasks')
    # if the form in the register page is valid, this funciton will be rendered 
    def form_valid(self, form):
        # if the form is valid, this function will be rendered
        # Then,this valid form is saved and assigned as user attribute 
        user=form.save() 
        # if the form is saved, user is not None
        if user is not None:
            # login the user after the registeration successfully, 
            # the self.request is send by user to login after the successfull registeration
            login(self.request, user)
        # in this case, the parent class is FormView, which is a built-in Django view
        # super is a built-in Python function that returns a proxy object that allows you to call methods of the parent class
        # so, this line is calling form_valid method of the FormView class, passing the form instance as an argument 
        # to return the validated form of the form 
        return super(RegisterPage, self).form_valid(form)
        
    def get(self, *args, **kwargs):
        # if the user is authenticated, it will redirect to the tasks page 
        if self.request.user.is_authenticated:
            return redirect('tasks')
        # to return username, password and same password attributes from the formView class
        return super(RegisterPage, self).get(*args, **kwargs)






    
# to override the post(sending data to the user from server) method to call the parent's post method(which handles the logout)
# then, redirect to the login page 
class CustomLogoutView(LogoutView): # CustomLogoutView class inherits from LogoutView 
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect('login')

class TaskList(LoginRequiredMixin, ListView):
    model=Task  
    context_object_name = 'tasks'

    # 'self' is a reference to the instance of the class 
    # **kwargs is a dictionary of keyword arguments that can be passed to the method 
    def get_context_data(self, **kwargs):
        # to call the 'get_context_data' method of the parent class(ListView) using the super() function
        # super function returns a proxy(temsili) object, that allows us to call methods of the parent class 
        # the get_context_data method of parent class returns a dictionary containing the default context data 
        context=super().get_context_data(**kwargs)
        # to add new key-value pair to the context dictionary 
        # so, we can access the red value using color variable 
        # self.request is an instance of the HttpRequest class, which represents the current HTTP request
        # it contains information about the request such as the user making the request the method used (GET, POST) THE URL and more 
        
        context['tasks']=context['tasks'].filter(user=self.request.user)
        # this line count the uncompleted tasks
        context['count']=context['tasks'].filter(complete=False).count()
        # search input is assigned to the task title which is tried to get from the database through search-area
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title_startswith=search_input)
        context['search_input']=search_input
        return context
    

class TaskDetail(LoginRequiredMixin, DetailView):
    model= Task
    context_object_name= 'task'
    # DetailView and ListView are generic view 
    # template_name attribute is used to specify the name of the template file that should be used 
    # below code line, tells Django to use a template file named task.html 
    # which is located in a directory named base within your app's template directory 
    template_name='base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView): 
    model=Task # to use Task object
    # fields attribute'value is changed from '__all__' to the '['title', 'description', 'complete']'
    # because able to create a task for any user, the user should log in 
    # after user logged in, there is no need to determine who owns the task again 
    fields= ['title', 'description', 'complete']

    # when we define a 'CreateView', Django automatically look for a template to render the form 
    # Django checks the 'template_name' attribute of the view, since it is not, falls back to the default behavior
    success_url=reverse_lazy('tasks')

    # self represents the super class(TaskCreate)
    # form represents the page which is opened when the add task is clicked on the browser 
    def form_valid(self,form):
        # if the form is invalid, we return the form to the user 
        # the user instance of the TaskCreate template is assigned to the user who request HttpRequeste or send valid form to the server currently
        form.instance.user=self.request.user # this line is used to determine who will own the task to be created 
        # this line render the conditions of valid form to able to create task   
        return super(TaskCreate, self).form_valid(form)
         
# UpdateView is view for updating an object, 
class TaskUpdate(LoginRequiredMixin, UpdateView): 
    model = Task # to use task object 
    fields=['title', 'description', 'complete']  # specifies all fields of the Task model should be included in the form 
    # sets the URL to redirect to after a successful update of an existing task 
    # in this case, it will redirect to the Tasklist view
    success_url=reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView): 
    model = Task # DeleteView class run for the task models 
    context_object_name='task' # the deleted object named as a task 
    success_url= reverse_lazy('tasks') # to direct tasks URL after the deletion of the task 

