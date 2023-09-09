from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from todo.models import Dash
from django import forms
from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['name', 'reminder_time']


class RegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["username","email","password1","password2"]


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password1=forms.CharField(label="password", widget=forms.PasswordInput(attrs={"class":"form-control"}))


class TaskForm(forms.ModelForm):

    class Meta:
        model=Dash
        fields=["task_name"]

class TaskChangeForm(forms.ModelForm):

    class Meta:
        model=Dash
        fields=["task_name","status"]
