# import calendar
# import json
# from celery import shared_task
# from django.utils import timezone
# from dateutil.relativedelta import relativedelta
# from crm.models import Reminder
#
# def send_reminder_test_def(reminder_id):
#     reminder = Reminder.objects.get(id=reminder_id)
#     print(f"Напоминание для задачи {reminder.task}")
#
# def should_send_daily(reminder, now):
#     """Проверка, нужно ли отправлять ежедневное напоминание"""
#     target_time = now.replace(
#         hour=reminder.custom_time.hour,
#         minute=reminder.custom_time.minute,
#         second=0
#     )
#     return (
#         now >= target_time and
#         (not reminder.last_reminder_sent or
#          now.date() > reminder.last_reminder_sent.date())
#     )
#
# def should_send_weekly(reminder, now):
#     """Проверка, нужно ли отправлять еженедельное напоминание"""
#     return (
#         now.weekday() == reminder.task.must_be_completed.weekday() and
#         now.time() >= reminder.custom_time and
#         (not reminder.last_reminder_sent or
#         (now - reminder.last_reminder_sent).days >= 7)
#     )
#
#
# def should_send_monthly(reminder, now):
#     # Получаем последний день текущего месяца
#     _, last_day_of_month = calendar.monthrange(now.year, now.month)
#
#     # Определяем день дедлайна с учётом месяца
#     task_deadline_day = reminder.task.must_be_completed_by.day
#     task_day = min(task_deadline_day, last_day_of_month)
#
#     # Проверяем условия
#     if now.day != task_day:
#         return False
#
#     if not reminder.last_reminder_sent:
#         return True
#
#     # Вычисляем следующую дату напоминания
#     last_sent_date = reminder.last_reminder_sent.date()
#     next_reminder_date = (last_sent_date + relativedelta(months=1)).replace(day=task_day)
#
#     # Корректируем, если task_day превышает дни в месяце next_reminder_date
#     _, next_last_day = calendar.monthrange(next_reminder_date.year, next_reminder_date.month)
#     next_reminder_date = next_reminder_date.replace(day=min(task_day, next_last_day))
#
#     return now.date() >= next_reminder_date
#
#
# def should_send_custom(reminder, now):
#     """Проверка, нужно ли отправлять кастомное напоминание"""
#     # Для тестирования отправляется reminder.custom_days в виде списка из админки.
#     if isinstance(reminder.custom_days, list):
#         custom_days = reminder.custom_days
#     else:
#         try:
#             custom_days = json.loads(reminder.custom_days)
#         except (TypeError, json.JSONDecodeError):
#             return False
#
#     day_mapping = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3,
#                    'fri': 4, 'sat': 5, 'sun': 6}
#     current_day = list(day_mapping.keys())[now.weekday()]
#
#     return (
#             current_day in custom_days and
#             now.time() >= reminder.custom_time and
#             (not reminder.last_reminder_sent or
#              now.date() > reminder.last_reminder_sent.date())
#     )
#
# @shared_task
# def check_daily_reminders():
#     """
#     Проверка ежедневных напоминаний.
#     Работает в celery beat раз в час.
#     """
#     reminders = Reminder.objects.filter(
#         is_active=True,
#         mode="daily"
#     ).exclude(task__expired=True)
#     now = timezone.localtime()
#     for reminder in reminders:
#         if should_send_daily(reminder, now):
#             # TODO: Тут логика отправки ежедневных напоминаний
#             # Обновление даты последней отправки
#             reminder.last_reminder_sent = now
#             reminder.save()
#
# @shared_task
# def check_weekly_reminders():
#     """
#     Проверка еженедельных напоминаний.
#     Работает в celery beat раз в два часа.
#     """
#     reminders = Reminder.objects.filter(
#         is_active=True,
#         mode="weekly"
#     ).exclude(task__expired=True)
#     now = timezone.localtime()
#     for reminder in reminders:
#         if should_send_weekly(reminder, now):
#             # TODO: Тут логика отправки еженедельных напоминаний
#             # Обновление даты последней отправки
#             reminder.last_reminder_sent = now
#             reminder.save()
#
# @shared_task
# def check_monthly_reminders():
#     """
#     Проверка ежемесячных напоминаний.
#     Работает в celery beat раз в день в 9:00.
#     """
#     reminders = Reminder.objects.filter(
#         is_active=True,
#         mode="monthly"
#     ).exclude(task__expired=True)
#     now = timezone.localtime()
#     for reminder in reminders:
#         if should_send_monthly:
#             # TODO: Тут логика отправки ежемесячных напоминаний.
#             reminder.last_reminder_sent = now
#             reminder.save()
#
#
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