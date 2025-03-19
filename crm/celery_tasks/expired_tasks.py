from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from crm.models import Task
from .notifications_tasks import one_hour_before_deadline_notification, notification_at_expired_task


@shared_task
def do_task_expired():
    """
    Поиск задач, у которых истек срок, и изменение их expired на True.
    Отправка оповещения о просрочке тех задач, у которых notifications = True.
    Задача запускается django-celery-beat раз в 2 минуты.
    """
    tasks = Task.objects.filter(
        must_be_completed_by__lt=timezone.localtime(),
        expired=False
    )

    # Постановка задач на отправку оповещения о просрочке
    for task in tasks:
        print(f"Перебираем задачи task: {task}")
        if task.notifications:
            notification_at_expired_task.delay(task.id)

    # Обновление expired
    tasks.update(expired=True)


@shared_task
def do_task_not_expired():
    """
    Поиск просроченных задач, у которых обновился срок исполнения.
    Изменение их expired обратно на False.
    Задача запускается django-celery-beat раз в 2 минуты.
    """
    Task.objects.filter(
        must_be_completed_by__gt=timezone.localtime(),
        expired=True
    ).update(expired=False)


@shared_task
def one_hour_before_task_expired():
    """
    Поиск задач, которые будут просрочены в течение часа.
    Запуск задач по оповещению менеджеров. Для оповещения задача должна быть notification=True
    После отправки оповещения before_one_hour_deadline_notification у задачи = True.
    Задача запускается django-celery-beat раз в 2 минуты.
    """
    one_hour_later = timezone.localtime() + timedelta(hours=1)

    tasks = Task.objects.filter(
        notifications=True,
        expired=False,
        must_be_completed_by__lte=one_hour_later,
        before_one_hour_deadline_notification=False,
    )
    for task in tasks:
        one_hour_before_deadline_notification.delay(task.id)
