"""Dashboardtodo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from todo import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignupView.as_view(),name="signup"),
    path('login/',views.SignInView.as_view(),name="signin"),
    path("logout/",views.sign_out_view,name="signout"),
    path("index/",views.IndexView.as_view(),name="dash"),
    path("todos/add/",views.TaskCreateView.as_view(),name="todo-add"),
    path("todos/list/",views.TaskListView.as_view(),name="task-list"),
    path("todos/<int:pk>/change",views.TaskEditView.as_view(),name="task-edit"),
    path("todos/<int:pk>/remove/",views.task_delete_view,name="task-delete"),
    path('reminders/add/', views.ReminderCreateView.as_view(), name='reminder_create'),
    path('reminders/', views.ReminderListView.as_view(), name='reminder_list'),
    path('weather/', views.weather_dashboard, name='weather_dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
