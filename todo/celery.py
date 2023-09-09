from celery import Celery
from celery.schedules import crontab

app = Celery('your_project_name')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send-reminders': {
        'task': 'todo.views.send_reminders',
        'schedule': crontab(minute='*'),  # Run every minute
    },
}