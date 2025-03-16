from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum, F, Q

from crm.models import Task
from crm.views import staff_required
from crm.permissions import ElementPermission
from crm.responses import json_response


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