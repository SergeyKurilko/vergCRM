from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from crm.models import Task, UserProfile
from .notifications_tasks import (one_hour_before_deadline_notification,
                                  notification_at_expired_task,
                                  one_workday_before_deadline_notification)

def get_previous_workday(date):
    """
    Получение предыдущего рабочего дня. Для оповещений о просрочке задачи за сутки,
    или за 3 дня, если сегодня пятница, а задача стоит на понедельник.
    """
    prev_day = date - timedelta(days=1)
    # Пока предыдущий день >= 5 (суббота (5), воскресенье (6)), понижаем доя пятницы.
    while prev_day.weekday() >= 5:
        prev_day -= timedelta(days=1)
    return prev_day


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


@shared_task
def one_workday_before_task_expired():
    """
    Поиск задач, которые будут просрочены на следующий рабочий день.
    Задача выполняется каждый день в 9 утра.
    """
    today = timezone.localtime().date()
    tasks = Task.objects.filter(
        notifications=True,
        expired=False,
        must_be_completed_by__gt=timezone.localtime(),
        before_one_workday_deadline_notification=False,
    )

    for task in tasks:
        deadline_date = task.must_be_completed_by.date()
        previous_workday = get_previous_workday(deadline_date)

        # Сегодня не предыдущий рабочий день -> пропускаем
        if previous_workday != today:
            continue

        manager_profile = UserProfile.objects.get(
            user_id=task.manager.id)

        # Проверяем, выпадает ли дедлайн на выходные
        is_deadline_weekend = deadline_date.weekday() >= 5

        # Отправляем уведомление, если:
        # 1. Дедлайн в будни ИЛИ
        # 2. Дедлайн в выходные, но пользователь разрешил такие уведомления
        if not is_deadline_weekend or manager_profile.day_off_notification:
            one_workday_before_deadline_notification.delay(task.id)
            task.before_one_workday_deadline_notification = True
            task.save()

