from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum, F, Q

from crm.models import Client, ServiceRequest
from crm.views import staff_required
from crm.permissions import ElementPermission
from crm.responses import json_response


class BaseClientView(ElementPermission):
    def get_client(self, request,
                   request_method: str = "GET",
                   with_active_service_requests_count: bool = False,
                   with_all_service_requests_count: bool = False
                   ) -> Client | JsonResponse:
        """
        Получает клиента по client_id и проверяет доступ менеджера.

        Args:
           request (WSGIRequest): объект запроса WSGIRequest.
           request_method (str): метод запроса "GET" или "POST". По-умолчанию "GET"
           with_active_service_requests_count (bool): аннотирует объект client дополнительно полем active_service_request_count.
           with_all_service_requests_count (bool): аннотирует объект полем all_service_requests_count
        Returns:
            Client | JsonResponse: Объект Client или JsonResponse с ошибкой.
        """
        client_id = None

        if request_method == "GET":
            client_id = request.GET.get('client_id')
        elif request_method == "POST":
            client_id = request.POST.get('client_id')

        if not client_id:
            return json_response.validation_error("Expected client_id")

        try:
            # Аннотация полем active_service_request_count
            if with_active_service_requests_count:
                client = Client.objects.annotate(
                    active_service_request_count=Count(
                        "service_requests",
                        filter=Q(service_requests__status="in_progress"))
                ).get(id=client_id)

            # Аннотация полем all_service_request_count
            elif with_all_service_requests_count:
                client = Client.objects.annotate(
                    all_service_request_count=Count("service_requests")
                ).get(id=client_id)
            else:
                client = Client.objects.get(id=client_id)
        except ValueError:
            return json_response.validation_error("Expected number.")
        except Client.DoesNotExist:
            return json_response.not_found_error("Client not found")

        if not self.verification_owner(request=request, obj=client):
            return json_response.manager_forbidden("Нет доступа к клиенту")

        return client


@method_decorator(staff_required, "dispatch")
class ClientListView(View):
    """
    Получение списка клиентов
    """

    def get(self, request):
        """
        Получает request, возвращает render clients-list.html
        В контексте список клиентов пользователя.
        """
        # TODO: Добавить поиск по имени и телефону
        clients = Client.objects.filter(
            manager=request.user
        )
        # Пагинация
        paginator = Paginator(clients, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "clients": page_obj,
        }

        return render(request, "crm/clients/clients-list.html", context)


@method_decorator(staff_required, "dispatch")
class ClientDetailView(BaseClientView, View):
    """
    Получение карточки клиента
    """

    def get(self, request):
        """
        Ожидает ajax-request. Возвращает html с модальным окном и карточкой клиента в нем.
        """
        client = self.get_client(
            request=request,
            request_method="GET",
            with_active_service_requests_count=True
        )

        # Если вместо объекта вернулся json, то возвращаем его клиенту
        if isinstance(client, JsonResponse):
            return client

        # Ожидаемая прибыль по всем заявкам клиента
        total_profit = (ServiceRequest.objects.filter(
            client=client, status="in_progress"
        )
        .annotate(
            profit=F("total_price") - F("cost_price")
        ).aggregate(
            total_profit=Sum("profit")
        ))["total_profit"] or 0

        # Общее количество заявок
        all_service_request_quantity = client.service_requests.all().count()

        context = {
            "client": client,
            "all_service_request_quantity": all_service_request_quantity,
            "total_profit": total_profit
        }

        # Создание html для модального окна с карточкой клиента
        modal_html = render_to_string(
            template_name="crm/clients/dynamic_modals/client-detail-modal.html",
            request=request,
            context=context
        )

        return JsonResponse({
            "success": True,
            "modal_html": modal_html
        })


@method_decorator(staff_required, "dispatch")
class ClientUpdateView(BaseClientView, View):
    """
    Обновление client
    """

    def post(self, request):
        """
        Получает post с формой для обновления клиента.
        """

        # Проверка наличия объекта и прав доступа к нему
        client = self.get_client(
            request=request,
            request_method="POST",
        )

        if isinstance(client, JsonResponse):
            return client

        required_keys = {
            "ClientName", "ClientPhone", "ClientWhatsapp", "ClientTelegram",
            "ClientEmail"
        }

        data = request.POST

        # Проверка наличия всех ожидаемых ключей в request.POST
        if not required_keys.issubset(set(data.keys())):
            return json_response.validation_error(
                message="Что-то пошло не так. Перезагрузите страницу"
            )

        update_client = {
            "name": data.get("ClientName"),
            "phone": data.get("ClientPhone"),
            "whatsapp": data.get("ClientWhatsapp"),
            "telegram": data.get("ClientTelegram"),
            "email": data.get("ClientEmail"),
        }

        for key, value in update_client.items():
            if value is not None:
                setattr(client, key, value)
            else:
                return json_response.validation_error(
                    "Форма не валидна"
                )

        return JsonResponse({
            "success": True
        })


@method_decorator(staff_required, "dispatch")
class ClientDeleteView(BaseClientView, View):
    """
    Удаление клиента
    """

    def get(self, request):
        """
        Получение модального окна с подтверждением удаления клиента
        """
        # Проверка наличия объекта и прав доступа к нему
        client = self.get_client(
            request=request,
            request_method="GET",
        )

        # Если вернулся JsonResponse с ошибкой, то тут ее возвращаем
        if isinstance(client, JsonResponse):
            return client

        modal_html = render_to_string(
            template_name="crm/clients/dynamic_modals/confirm-delete-client-modal.html",
            request=request,
            context={"client": client}
        )

        return JsonResponse({
            "success": True,
            "modal_html": modal_html
        })

    def post(self, request) -> JsonResponse:
        """
        Ожидает POST с формой c input name = client_id.
        Удаляет объект Client
        """
        client = self.get_client(
            request=request,
            request_method="POST",
            with_all_service_requests_count=True
        )

        if isinstance(client, JsonResponse):
            return client

        if client.all_service_request_count > 0:
            return JsonResponse({
                "error": True,
                "message": f"У этого клиента есть заявки. "
                           f"Количество заявок: {client.all_service_request_count}шт. "
                           f"Сначала удалите их, чтобы удалить клиента."
            }, status=403)
        # client.delete()

        return JsonResponse({
            "success": True
        })
