from celery import shared_task
from crm.models import Task

@shared_task
def one_workday_before_deadline_notification(task_id: int):
    """
    Отправка сообщения о том, что задача будет просрочена на следующий рабочий день.
    """
    task = Task.objects.get(id=task_id)
    manager = task.manager
    # TODO: проверить настройки оповещения менеджера и отправить письмо /или/ телеграм
    print(f"Напоминание! Задача {task.title} должна "
          f"быть выполнена до {task.must_be_completed_by.strftime('%d.%m.%Y %H:%M')}")
    task.before_one_workday_deadline_notification = True
    task.save()

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