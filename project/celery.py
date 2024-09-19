import os
from celery import Celery

environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'project.settings.{environment}')

app = Celery('project')

LOG_DIR = os.path.join('project', 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    
CELERY_LOG_FILE = os.path.join(LOG_DIR, 'celery.log')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')