from celery import shared_task
from django.contrib.sites.models import Site
from django.db.models import Q

from crm.models import Reminder, Task
from crm.celery_tasks.send_reminders_tasks import send_once_reminder, send_recurring_reminder
from datetime import datetime
from django.utils import timezone


@shared_task
def check_once_reminders():
    """
    Проверка наличия разовых напоминаний для отправки.
    Проверка работает в celery beat раз в минуту.
    """
    reminders = Reminder.objects.filter(
        is_active=True,
        mode="once"
    ).select_related('task').exclude(task__expired=True)

    now = timezone.localtime()
    for r in reminders:
        if r.scheduled_datetime <= now:
            send_once_reminder.delay(reminder_id=r.id)


@shared_task
def recurring_reminders_check():
    now = timezone.localtime()

    # Повторяющиеся напоминания, кроме тех, у которых задача просрочена,
    # ИЛИ напоминание сегодня уже отправлялось
    reminders = Reminder.objects.filter(
        is_active=True,
        mode="recurring"
    ).select_related('task').exclude(
        Q(task__expired=True) |
        Q(last_reminder_sent__date=now.date())
    )


    now_day = now.strftime("%a").lower()
    now_time = now.time()

    for r in reminders:
        if now_day in r.recurring_days and now_time > r.recurring_time:
            send_recurring_reminder(reminder_id=r.id)




# @shared_task
# def check_custom_reminders():
#     """
#     Проверка ежемесячных напоминаний.
#     Работает в celery beat раз в минуту.
#     """
#     reminders = Reminder.objects.filter(
#         is_active=True,
#         mode="custom"
#     ).exclude(task__expired=True)
#     now = timezone.localtime()
#     for reminder in reminders:
#         if should_send_custom(reminder, now):
#             # TODO: Тут логика отправки кастомного напоминания
#             send_reminder_test_def(reminder.id)
#             # Обновление даты последней отправки напоминания
#             reminder.last_reminder_sent = now
#             reminder.save()