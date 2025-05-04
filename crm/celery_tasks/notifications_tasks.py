from celery import shared_task
from django.conf import settings

from crm.models import Task
from telegram_bot.sender_bot.task_notifications_senders import (send_telegram_notification_before_expire_task,
                                                                send_telegram_notification_at_expire_task)
from crm.celery_tasks.make_display_notifications_tasks import (one_workday_before_deadline_display_notification,
                                                               one_hour_before_deadline_display_notification,
                                                               at_expired_task_display_notification)

weekdays_mapping = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}

@shared_task
def one_workday_before_deadline_notification(task_id: int):
    """
    Отправка сообщения о том, что задача будет просрочена на следующий рабочий день.
    """
    task = Task.objects.get(id=task_id)
    telegram_id = task.manager.userprofile.telegram_id

    # Получаем текущий домен
    domain = settings.BASE_URL
    task_absolute_url = f"{domain}{task.get_absolute_url()}"

    message = (
        f"⏳ Задача: '{task.title}' будет просрочена "
        f"{task.must_be_completed_by.strftime('%d.%m.%Yг. в %H:%M')} "
        f"({weekdays_mapping.get(task.must_be_completed_by.weekday())}).\n"
    )

    # Постановка задачи на создание DisplayNotification
    one_workday_before_deadline_display_notification.delay(
        task_id=task.id
    )

    # Постановка задачи на отправку оповещения в тг
    send_telegram_notification_before_expire_task.delay(
        chat_id=telegram_id,
        message=message,
        task_url=task_absolute_url
    )
    task.before_one_workday_deadline_notification = True
    task.save()

@shared_task
def one_hour_before_deadline_notification(task_id: int):
    """
    Отправка сообщения менеджеру о том, что задача будет просрочена в течение часа.
    """
    task = Task.objects.get(id=task_id)
    telegram_id = task.manager.userprofile.telegram_id

    # Получаем текущий домен
    domain = settings.BASE_URL
    task_absolute_url = f"{domain}{task.get_absolute_url()}"

    message = (
        f"⏳ Задача: {task.title} будет просрочена в течение часа.\n"
    )

    # Задача на создание DisplayNotification
    one_hour_before_deadline_display_notification.delay(
        task_id=task.id
    )

    send_telegram_notification_before_expire_task.delay(
        chat_id=telegram_id,
        message=message,
        task_url=task_absolute_url
    )
    task.before_one_hour_deadline_notification = True
    task.save()


@shared_task
def notification_at_expired_task(task_id: int):
    """
        Отправка сообщения менеджеру о том, что задача просрочена сейчас.
    """
    task = Task.objects.get(id=task_id)
    telegram_id = task.manager.userprofile.telegram_id

    # Получаем текущий домен
    domain = settings.BASE_URL
    task_absolute_url = f"{domain}{task.get_absolute_url()}"

    message = (
        f"🚨 Просрочена задача: {task.title}"
    )

    # Задача на создание DisplayNotification
    at_expired_task_display_notification.delay(
        task_id=task.id
    )

    send_telegram_notification_at_expire_task.delay(
        chat_id=telegram_id,
        message=message,
        task_url=task_absolute_url,
        task_id=task_id
    )