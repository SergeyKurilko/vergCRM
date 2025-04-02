from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum, F, Q

from crm.models import Task
from crm.responses import json_response
from crm.views import staff_required
from crm.permissions import ElementPermission


class BaseTaskView(ElementPermission):
    def get_task(self, request, task_id: int) -> Task | HttpResponse:
        """
        Получает задачу по task_id и проверяет доступ менеджера к задаче.

        Args:
           request (WSGIRequest): объект запроса WSGIRequest.
           request_method (str): метод запроса "GET" или "POST". По-умолчанию "GET"
        Returns:
            Task | JsonResponse: Объект Task или JsonResponse с ошибкой.
        """

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponse("Task not found", status=404)

        if not self.verification_owner(request=request, obj=task):
            return HttpResponse("Нет доступа к задаче", status=403)

        return task


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
            Task | JsonResponse: Объект Task или JsonResponse с ошибкой.
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

