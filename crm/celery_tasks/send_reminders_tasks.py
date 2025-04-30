from celery import shared_task
from django.conf import settings

from crm.models import Reminder, Task
from telegram_bot.sender_bot.task_reminders_senders import (
    send_telegram_once_reminder,
    send_telegram_recurring_reminder
)


@shared_task
def send_once_reminder(reminder_id: int):
    """
    Отправка сообщений с разовыми напоминаниями.
    Предусматривает расширение (другие мессенджеры, email и т.д.)
    """
    reminder = Reminder.objects.get(id=reminder_id)

    task = Task.objects.get(id=reminder.task.id)
    telegram_id = task.manager.userprofile.telegram_id

    # Получаем текущий домен
    domain = settings.BASE_URL
    absolute_url = f"{domain}/{task.get_absolute_url()}"


    send_telegram_once_reminder.delay(
        chat_id=telegram_id,
        task_url=absolute_url,
        task_title=task.title
    )


@shared_task
def send_recurring_reminder(reminder_id: int):
    """
    Отправка сообщений с повторяющимися напоминаниями.
    Предусматривает расширение (другие мессенджеры, email и т.д.)
    """
    reminder = Reminder.objects.select_related('task').get(id=reminder_id)
    task = Task.objects.get(id=reminder.task.id)

    telegram_id = reminder.task.manager.userprofile.telegram_id

    # Получаем текущий домен
    domain = settings.BASE_URL
    absolute_url = f"{domain}/{reminder.task.get_absolute_url()}"

    send_telegram_recurring_reminder.delay(
        chat_id=telegram_id,
        task_url=absolute_url,
        task_title=task.title,
        reminder_id=reminder.id,
    )
