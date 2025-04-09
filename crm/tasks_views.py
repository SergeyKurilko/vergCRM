from datetime import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum, F, Q, Prefetch

from crm.models import Task, Reminder
from crm.responses import json_response
from crm.views import staff_required
from crm.permissions import ElementPermission


class BaseTaskView(ElementPermission):
    def get_task(self, request, task_id: int) -> Task | HttpResponse:
        """
        Получает задачу по task_id и проверяет доступ менеджера к задаче.

        Args:
           request (WSGIRequest): объект запроса WSGIRequest.
           task_id (int): id задачи
        Returns:
            Task | HttpResponse: Объект Task или HttpResponse с ошибкой.
        """

        try:
            task = Task.objects.prefetch_related(
                Prefetch(
                    'reminders',
                    queryset=Reminder.objects.filter(is_active=True))
            ).get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponse("Task not found", status=404)

        if not self.verification_owner(request=request, obj=task):
            return HttpResponse("Нет доступа к задаче", status=403)

        return task

    def check_task_form(self, request) -> dict | JsonResponse:
        """
        Проверка обязательных полей у формы для создания или изменения существующей task

        Args:
           request (WSGIRequest): объект запроса WSGIRequest.
        Returns:
            dict | HttpResponse: Словарь с параметрами для распаковки или JsonResponse с ошибкой.
        """
        # TODO: описать метод. Использовать для TaskUpdateView и TaskCreateView
        pass



@method_decorator(staff_required, "dispatch")
class TaskListView(View):
    """
    Получение списка задач
    """
    def get(self, request):
        """
        Получает request, возвращает render tasks-list.html
        В контексте список задач пользователя.
        """
        tasks = Task.objects.filter(
            manager=request.user
        )
        # Пагинация
        paginator = Paginator(tasks, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "tasks": page_obj,
        }

        return render(request, "crm/tasks/tasks-list.html", context)


@method_decorator(staff_required, "dispatch")
class TaskDetailView(BaseTaskView, View):
    """
    Просмотр задачи на отдельной странице
    """
    def get(self, request, task_id):
        """
        Получает GET-запрос с параметром task_id. Возвращает рендер страницы с задачей

        Args:
           request (WSGIRequest): объект запроса WSGIRequest.
        Returns:
            Task | HttpResponse: Объект Task или HttpResponse с ошибкой.
        """
        task = self.get_task(request, task_id=task_id)


        # Если вместо объекта вернулся HttpResponse с ошибкой, то возвращаем его клиенту
        if isinstance(task, HttpResponse):
            return task

        return render(
            request=request,
            template_name='crm/tasks/task-detail.html',
            context={"task": task}
        )

@method_decorator(staff_required, "dispatch")
class TaskDeleteView(View):
    def get(self, request):
        """
        Получение модального окна для удаления задачи (на отдельной странице)
        """
        task_id = request.GET.get("task_id")
        if not task_id:
            return json_response.validation_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return json_response.not_found_error(
                "Задача не найдена"
            )

        if task.manager.id != request.user.id:
            return json_response.manager_forbidden(
                "Менеджер не привязан к задаче."
            )

        context = {
            "task": task
        }

        new_content = render_to_string(
            template_name="crm/tasks/dynamic_modals/confirm-delete-task-modal.html",
            request=request,
            context=context
        )

        return JsonResponse({
            "success": True,
            "new_content": new_content
        })

    def post(self, request):
        """
        Удаление задачи (на отдельной странице)
        """
        task_id = request.POST.get("delete_task_id")
        if not task_id:
            return json_response.validation_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return json_response.not_found_error(
                "Задача не найдена"
            )

        if request.user.id != task.manager.id:
            return json_response.manager_forbidden(
                "Задача не принадлежит менеджеру"
            )

        task.delete()

        return JsonResponse({
            "success": True,
            "url_for_redirect": reverse("crm:tasks_list")
        }, status=200)


@method_decorator(staff_required, "dispatch")
class TaskUpdateView(BaseTaskView, View):
    def post(self, request):
        """
        Редактирование задачи (на отдельной странице)
        """
        data = request.POST
        required_fields = {
            "manager_id", "task_id",
            "title", "text", "must_be_completed_by"
        }

        # Извлечение данных из тела запроса
        manager_id = data.get("manager_id")
        task_id = data.get("task_id")
        title = data.get("title")
        text = data.get("text")
        must_be_completed_by = data.get("must_be_completed_by")
        notifications = data.get("notifications")

        if not request.user.id == int(manager_id):
            return json_response.manager_forbidden(
                message="Клиент не привязан к менеджеру"
            )

        # Проверка наличия всех обязательных полей
        if not required_fields.issubset(set(data.keys())):
            return json_response.validation_error(
                message="Что-то пошло не так. Перезагрузите страницу"
            )

        if (not title or not text) or (len(title) < 5 or len(text) < 5):
            return json_response.validation_error(
                "Название и текст должны быть не короче 5 симв."
            )

        # Проверка наличия и длины даты
        if not must_be_completed_by or len(must_be_completed_by) < 16:
            return json_response.validation_error(
                "Вы не указали дату."
            )

        # Ищем задачу для обновления
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return json_response.not_found_error(
                message="Задача не найдена."
            )

        # Преобразуем строку must_be_completed_by в datetime
        try:
            must_be_completed_by = datetime.strptime(must_be_completed_by, '%d.%m.%Y %H:%M')
        except ValueError:
            # Обработка ошибки, если формат неверный
            return json_response.validation_error(
                "Неверный формат даты"
            )

        # Включен ли toggle напоминания у задачи
        task_notifications = True if notifications else False

        task.title = title
        task.text = text
        task.must_be_completed_by = must_be_completed_by
        task.notifications = task_notifications

        task.save()

        # Поиск добавленных reminders
        new_reminders = []
        for key, value in data.items():
            if key.startswith('reminderMode-'):
                index = key.split("-")[1]

                # Если это разовый reminder
                if value == 'once':
                    # Извлекаем reminder_once_datetime и преобразуем строку scheduled_datetime в datetime
                    try:
                        scheduled_datetime = (
                            datetime.strptime(data.get(f"reminder_once_datetime-{index}"), '%d.%m.%Y %H:%M'))
                    except ValueError:
                        # Обработка ошибки, если формат неверный
                        return json_response.validation_error(
                            "Неверный формат даты у напоминания"
                        )
                    once_reminder = Reminder(
                        task=task,
                        mode='once',
                        scheduled_datetime=scheduled_datetime
                    )
                    new_reminders.append(once_reminder)

                # Если это recurring reminder
                elif value == "recurring":
                    # Извлекаем time и преобразуем в корректный datetime.time
                    try:
                        time_str = data.get(f"reminder_recurring_time-{index}")
                        time_obj = datetime.strptime(time_str, '%H:%M').time()
                    except ValueError:
                        # Обработка ошибки, если формат неверный
                        return json_response.validation_error(
                            "Неверный формат даты у напоминания"
                        )

                    recurring_days = []
                    day_mapping = {
                        'mon': 'mon',
                        'tue': 'tue',
                        'wed': 'wed',
                        'thu': 'thu',
                        'fri': 'fri',
                        'sat': 'sat',
                        'sun': 'sun'
                    }

                    for day_key, day_value in data.items():
                        if (day_key.startswith(
                                tuple(day_mapping.keys())) and
                                day_key.endswith(f"-{index}")
                        ):
                            day_name = day_key.split("-")[0]
                            recurring_days.append(day_name)

                    recurring_reminder = Reminder(
                        task=task,
                        mode='recurring',
                        recurring_time=time_obj,
                        recurring_days=recurring_days
                    )
                    new_reminders.append(recurring_reminder)

        Reminder.objects.bulk_create(new_reminders)

        return JsonResponse({
            "success": True,
        })


@method_decorator(staff_required, "dispatch")
class TaskCreateView(BaseTaskView, View):
    """
    Создание задачи (на отдельной странице)
    """
    def get(self, request: WSGIRequest):
        """
        Принимает ajax-запрос, возвращает модальное окно для создания задачи.

        Args:
            request (WSGIRequest): объект запроса WSGIRequest
        Returns:
            JsonResponse (JsonResponse): html код с модальным окном или ошибку
        """
        context = {
            "manager_id": request.user.id
        }
        new_task_modal = render_to_string(
            template_name="crm/tasks/dynamic_modals/modal-for-add-new-task.html",
            request=request,
            context=context
        )

        return JsonResponse({
            "success": True,
            "new_task_modal": new_task_modal
        })

    def post(self, request):
        data = request.POST
        required_fields = {
            "manager_id",
            "title", "text", "must_be_completed_by"
        }
        # Проверка наличия всех обязательных полей
        if not required_fields.issubset(set(data.keys())):
            return json_response.validation_error(
                message="Что-то пошло не так. Перезагрузите страницу"
            )

        # Извлечение данных из тела запроса
        manager_id = data.get("manager_id")
        title = data.get("title")
        text = data.get("text")
        must_be_completed_by = data.get("must_be_completed_by")
        notifications = data.get("notifications")

        if not manager_id:
            return json_response.validation_error(
                "Expected manager_id"
            )

        if (not title or not text) or (len(title) < 5 or len(text) < 5):
            return json_response.validation_error(
                "Название и текст должны быть не короче 5 симв."
            )

        # Проверка наличия и длины даты
        if not must_be_completed_by or len(must_be_completed_by) < 16:
            return json_response.validation_error(
                "Вы не указали дату."
            )

        # Преобразуем строку must_be_completed_by в datetime
        try:
            must_be_completed_by = datetime.strptime(must_be_completed_by, '%d.%m.%Y %H:%M')
        except ValueError:
            # Обработка ошибки, если формат неверный
            return json_response.validation_error(
                "Неверный формат даты"
            )

        # Включен ли toggle напоминания у задачи
        task_notifications = True if notifications else False

        new_task = Task.objects.create(
            title=title,
            text=text,
            manager_id=manager_id,
            must_be_completed_by=must_be_completed_by,
            notifications=task_notifications
        )

        # Поиск reminders
        new_reminders = []
        for key, value in data.items():
            if key.startswith('reminderMode-'):
                index = key.split("-")[1]

                # Если это разовый reminder
                if value == 'once':
                    # Извлекаем reminder_once_datetime и преобразуем строку scheduled_datetime в datetime
                    try:
                        scheduled_datetime = (
                            datetime.strptime(data.get(f"reminder_once_datetime-{index}"), '%d.%m.%Y %H:%M'))
                    except ValueError:
                        # Обработка ошибки, если формат неверный
                        return json_response.validation_error(
                            "Неверный формат даты у напоминания"
                        )
                    once_reminder = Reminder(
                        task=new_task,
                        mode='once',
                        scheduled_datetime=scheduled_datetime
                    )
                    new_reminders.append(once_reminder)

                # Если это recurring reminder
                elif value == "recurring":
                    # Извлекаем time и преобразуем в корректный datetime.time
                    try:
                        time_str = data.get(f"reminder_recurring_time-{index}")
                        time_obj = datetime.strptime(time_str, '%H:%M').time()
                    except ValueError:
                        # Обработка ошибки, если формат неверный
                        return json_response.validation_error(
                            "Неверный формат даты у напоминания"
                        )

                    recurring_days = []
                    day_mapping = {
                        'mon': 'mon',
                        'tue': 'tue',
                        'wed': 'wed',
                        'thu': 'thu',
                        'fri': 'fri',
                        'sat': 'sat',
                        'sun': 'sun'
                    }

                    for day_key, day_value in data.items():
                        if (day_key.startswith(
                                tuple(day_mapping.keys())) and
                                day_key.endswith(f"-{index}")
                        ):
                            day_name = day_key.split("-")[0]
                            recurring_days.append(day_name)

                    recurring_reminder = Reminder(
                        task=new_task,
                        mode='recurring',
                        recurring_time=time_obj,
                        recurring_days=recurring_days
                    )
                    new_reminders.append(recurring_reminder)

        Reminder.objects.bulk_create(new_reminders)

        return JsonResponse({
            "success": True,
        }, status=200)


class MakeTaskIsCompletedView(View):
    """
    Завершить задачу.
    """
    def get(self, request: WSGIRequest):
        """
        Получение модального окна для завершения задачи (на отдельной странице)
        """
        task_id = request.GET.get("task_id")
        if not task_id:
            return json_response.validation_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return json_response.not_found_error(
                "Задача не найдена"
            )

        if task.manager.id != request.user.id:
            return json_response.manager_forbidden(
                "Менеджер не привязан к задаче."
            )

        context = {
            "task": task
        }

        new_content = render_to_string(
            template_name="crm/tasks/dynamic_modals/confirm-make-task-is-completed.html",
            request=request,
            context=context
        )

        return JsonResponse({
            "success": True,
            "new_content": new_content
        })

    def post(self, request):
        """
        Завершение задачи (на отдельной странице)
        """
        task_id = request.POST.get("complete_task_id")
        if not task_id:
            return json_response.validation_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        try:
            task = Task.objects.prefetch_related(
                "reminders"
            ).get(id=task_id)
        except Task.DoesNotExist:
            return json_response.not_found_error(
                "Задача не найдена"
            )

        if task.is_completed:
            return json_response.validation_error(
                "Задача уже завершена."
            )

        if request.user.id != task.manager.id:
            return json_response.manager_forbidden(
                "Задача не принадлежит менеджеру"
            )

        # Выключаем напоминания, если есть
        task.reminders.all().update(is_active=False)

        task.is_completed = True
        task.expired = False
        task.before_one_hour_deadline_notification = False
        task.before_one_workday_deadline_notification = False
        task.save()


        return JsonResponse({
            "success": True,
            "url_for_redirect": task.get_absolute_url()
        }, status=200)


class ResumeTaskView(View):
    """
    Вернуть завершенную задачу в работу
    """
    def get(self, request):
        """
        Получение модального окна для возвращения задачи в работу.
        """
        task_id = request.GET.get("task_id")
        if not task_id:
            return json_response.validation_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return json_response.not_found_error(
                "Задача не найдена"
            )

        if task.manager.id != request.user.id:
            return json_response.manager_forbidden(
                "Менеджер не привязан к задаче."
            )

        context = {
            "task": task
        }

        new_content = render_to_string(
            template_name="crm/tasks/dynamic_modals/confirm-task-resume.html",
            request=request,
            context=context
        )

        return JsonResponse({
            "success": True,
            "new_content": new_content
        })

    def post(self, request):
        """
        Возобновление задачи
        """
        task_id = request.POST.get("resume_task_id")
        if not task_id:
            return json_response.validation_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        try:
            task = Task.objects.prefetch_related(
                "reminders"
            ).get(id=task_id)
        except Task.DoesNotExist:
            return json_response.not_found_error(
                "Задача не найдена"
            )

        if request.user.id != task.manager.id:
            return json_response.manager_forbidden(
                "Задача не принадлежит менеджеру"
            )

        # Включаем напоминания, если еще есть
        task.reminders.all().update(is_active=True)

        task.is_completed = False
        task.expired = False
        task.before_one_hour_deadline_notification = False
        task.before_one_workday_deadline_notification = False
        task.save()


        return JsonResponse({
            "success": True,
        }, status=200)