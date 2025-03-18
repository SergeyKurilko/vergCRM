from celery import shared_task
from django.utils import timezone
from crm.models import Task

@shared_task
def do_task_expired():
    """
    Поиск задач, у которых истек срок, и изменение их expired на True.
    Задача запускается django-celery-beat раз в 5 минут.
    """
    print(timezone.localtime())
    Task.objects.filter(
        must_be_completed_by__lt=timezone.localtime(),
        expired=False
    ).update(expired=True)