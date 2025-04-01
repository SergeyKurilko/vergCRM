from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
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
