import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChatBot.settings')

app = Celery('webChatBot')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.autodiscover_tasks()
