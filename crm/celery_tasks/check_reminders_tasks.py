from celery import shared_task
from django.contrib.sites.models import Site
from django.db.models import Q

from crm.models import Reminder, Task
from crm.celery_tasks.send_reminders_tasks import send_once_reminder, send_recurring_reminder
from crm.celery_tasks.make_display_notifications_tasks import reminder_display_notification
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
            reminder_display_notification.delay(reminder_id=r.id)
            send_once_reminder.delay(reminder_id=r.id)
            r.is_active = False
            r.save()


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
            send_recurring_reminder.delay(reminder_id=r.id)
            reminder_display_notification.delay(reminder_id=r.id)

            r.last_reminder_sent = now
            r.save()


#shared_task
def check_old_inactive_reminders():
    # TODO: описать check_old_inactive_reminders
    # поиск и удаление напоминаний, у которых is_active = False и последний показ был месяц назад и более
    pass