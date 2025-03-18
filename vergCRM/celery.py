import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vergCRM.settings')

app = Celery("vergCRM")
app.config_from_object('django.conf:settings', namespace="CELERY")
# app.autodiscover_tasks()

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Указываем Celery, где искать задачи
app.autodiscover_tasks(['crm.celery_tasks'])