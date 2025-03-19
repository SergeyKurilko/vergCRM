from celery import shared_task
from crm.models import Task


@shared_task
def one_hour_before_deadline_notification(task_id: int):
    """
    Отправка сообщения менеджеру о том, что задача будет просрочена в течение часа.
    """
    task = Task.objects.get(id=task_id)
    manager = task.manager
    print(f"Задача {task.title} будет просрочена в течение часа!")
    task.before_one_hour_deadline_notification = True
    task.save()


@shared_task
def notification_at_expired_task(task_id: int):
    """
        Отправка сообщения менеджеру о том, что задача просрочена сейчас.
    """
    task = Task.objects.get(id=task_id)
    manager = task.manager
    print(f"ОПОВЕЩЕНИЕ! Задача {task.title} просрочена сейчас!")