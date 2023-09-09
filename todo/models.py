from django.db import models
from django.contrib.auth.models import User

class Dash(models.Model):
    task_name=models.CharField(max_length=120)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.task_name
    
class Reminder(models.Model):
    name = models.CharField(max_length=255)
    reminder_time = models.DateTimeField()