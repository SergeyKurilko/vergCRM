from celery import shared_task
from django.shortcuts import get_object_or_404

from crm.models import DisplayNotification, Task

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
        f"({weekdays_mapping.get(task.must_be_completed_by.weekday())}.\n"
        f"🔗 [Открыть задачу]({task.get_absolute_url()})"
    )