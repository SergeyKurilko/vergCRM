from celery import shared_task
from django.shortcuts import get_object_or_404

from crm.models import DisplayNotification, Task, Reminder

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
def one_workday_before_deadline_display_notification(task_id: int):
    """
    Экранное оповещение о том, что задача будет просрочена на следующий рабочий день.
    """
    notification_type = "one_workday_before_task_expired"
    task = get_object_or_404(
        Task, id=task_id
    )
    DisplayNotification.objects.create(
        user=task.manager,
        type=notification_type,
        message=
        f'⏳ Задача: "{task.title}" будет просрочена '
        f"{task.must_be_completed_by.strftime('%d.%m.%Yг. в %H:%M')} "
        f"({weekdays_mapping.get(task.must_be_completed_by.weekday())}).\n",
        link_text="Открыть задачу",
        link_url=task.get_absolute_url()
    )

@shared_task
def one_hour_before_deadline_display_notification(task_id):
    """
    Экранное оповещение о том, что задача будет просрочена в течение часа.
    """
    notification_type = "one_hour_before_task_expired"
    task = get_object_or_404(
        Task, id=task_id
    )
    DisplayNotification.objects.create(
        user=task.manager,
        type=notification_type,
        message=
        f'⏳ Задача: "{task.title}" будет просрочена в течение часа.',
        link_text="Открыть задачу",
        link_url=task.get_absolute_url()
    )

@shared_task
def at_expired_task_display_notification(task_id):
    """
    Экранное оповещение о том, что задача просрочена сейчас!
    """
    notification_type = "on_task_expired"
    task = get_object_or_404(
        Task, id=task_id
    )
    DisplayNotification.objects.create(
        user=task.manager,
        type=notification_type,
        message=
        f'🚨🚨🚨 Задача: "{task.title}" просрочена.',
        link_text="Открыть задачу",
        link_url=task.get_absolute_url()
    )

@shared_task
def reminder_display_notification(reminder_id):
    """
    Экранное оповещение с напоминанием о задаче.
    """
    reminder = Reminder.objects.select_related('task').get(id=reminder_id)
    notification_type = "reminder"
    DisplayNotification.objects.create(
        user=reminder.task.manager,
        type=notification_type,
        message=
        f"⏰ Напоминание о задаче: {reminder.task.title}\n",
        link_text="Открыть задачу",
        link_url=reminder.task.get_absolute_url()
    )

