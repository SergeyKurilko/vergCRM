from celery import shared_task
from django.contrib.sites.models import Site

from crm.models import Reminder, Task
from telegram_bot.task_reminders_senders import send_telegram_reminder
from django.utils import timezone

@shared_task
def send_once_reminder(reminder_id: int):
    reminder = Reminder.objects.get(id=reminder_id)

    task = Task.objects.get(id=reminder.task.id)
    telegram_id = task.manager.userprofile.telegram_id

    # Получаем текущий домен
    domain = Site.objects.get_current().domain
    absolute_url = f"https://{domain}{task.get_absolute_url()}"

    message = (
        f"⏰ Напоминание о задаче: {task.title}\n"
        f"🔗 [Открыть задачу]({absolute_url})"
    )

    send_telegram_reminder.delay(
        chat_id=telegram_id,
        message=message
    )

    reminder.delete()


@shared_task
def send_recurring_reminder(reminder_id: int):
    now = timezone.localtime()

    reminder = Reminder.objects.get(id=reminder_id)

    task = Task.objects.get(id=reminder.task.id)
    telegram_id = task.manager.userprofile.telegram_id

    # Получаем текущий домен
    domain = Site.objects.get_current().domain
    absolute_url = f"https://{domain}{task.get_absolute_url()}"

    message = (
        f"⏰ Напоминание о задаче: {task.title}\n"
        f"🔗 [Открыть задачу]({absolute_url})"
    )

    send_telegram_reminder.delay(
        chat_id=telegram_id,
        message=message
    )

    reminder.last_reminder_sent = now
    reminder.save()