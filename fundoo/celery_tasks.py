from __future__ import absolute_import
import os
import sys
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo.settings')

#app = Celery('fundoo')
sys.path.append(os.path.abspath('fundoo'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo.settings')
app = Celery('fundoo',
             broker='pyamqp://guest@localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#@app.task(bind=True)
#def debug_task(self):
#    print("Hello")