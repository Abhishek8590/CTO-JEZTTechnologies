

from django.shortcuts import render,redirect
from django.views.generic import View,FormView,CreateView,TemplateView,ListView,UpdateView,DetailView
from todo.forms import TaskForm,TaskChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from todo.models import Dash
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Reminder
from django.contrib.auth import authenticate, login, logout
from .forms import ReminderForm,LoginForm,RegistrationForm
import requests
from django.shortcuts import render
from django.conf import settings
# imported reverze laz to give success url
# since we are decorating a view instead of function we import method_decorator



    
def signin_required(fn):

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, "you must login to perform this action !!!")
            return redirect("signin")
        else:
            return fn(request, *args, **kwargs)
    return wrapper


# Create your views here.
class SignupView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "reg.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request, "account has been created !!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "failed to create account")
        return super().form_invalid(form)


class SignInView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password1")
            usr = authenticate(request, username=uname, password=pwd)
            if usr:
                login(request, usr)
                return redirect("dash")
            messages.error(request, "invalid credentials")
        return render(request, self.template_name, {"form": form})


        
    



# template inheritance
@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    # by inheriting django build in  Template view we make code less
    template_name="dash.html"


        
    
# localhost:8000/todos/add/
@method_decorator(signin_required,name="dispatch")
class TaskCreateView(CreateView):
    model=Dash
    form_class=TaskForm
    template_name="todo-add.html"
    success_url=reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Todo added successfully")
        return super().form_valid(form)


@method_decorator(signin_required,name="dispatch")
class TaskListView(ListView):
    model=Dash
    template_name="todo-list.html"
    context_object_name="tasks"
    # we have to change orm query cuz we dont need all objects in the list
    def get_queryset(self):
        return Dash.objects.filter(user=self.request.user).order_by("-created_date")
  
# localhost:8000/todos/<int-pk>/change
@method_decorator(signin_required,name="dispatch")
class TaskEditView(UpdateView):
    model=Dash
    form_class=TaskChangeForm
    template_name="task-edit.html"
    success_url=reverse_lazy("task-list")
   
@signin_required
def task_delete_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    obj=Dash.objects.get(id=id)
    if obj.user == request.user:
        Dash.objects.get(id=id).delete()
        messages.success(request,"task removed")
        return redirect("task-list")
    else:
        messages.error(request,"you don't have the permission")
        return redirect("signin")   




def signout_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"logged out")
    return redirect("signin")




@method_decorator(signin_required,name="dispatch") 
class ReminderCreateView(CreateView):
    model=Reminder
    form_class=ReminderForm
    template_name="addreminder.html"
    success_url=reverse_lazy("reminder_list")

    #to add extra details in form before save
    def form_valid(self, form):
        form.instance.user=self.request.user
        
        
        messages.success(self.request,"reminder has been created")
        return super().form_valid(form)


@method_decorator(signin_required,name="dispatch")
class ReminderListView(ListView):
    model = Reminder
    
    template_name='reminderslist.html'
    context_object_name = 'tasks'


    

def sign_out_view(request,*args,**kargs):
    logout(request)
    return redirect("signin")



def weather_dashboard(request):
    api_key = settings.OPENWEATHERMAP_API_KEY
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami']
    
    weather_data = []

    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        try:
            response = requests.get(url)
            data = response.json()
            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
            }
        except Exception as e:
            weather = {
                'city': city,
                'temperature': 'N/A',
                'description': str(e),
            }
        
        weather_data.append(weather)

    return render(request, 'Weatherr.html', {'weather_data': weather_data})