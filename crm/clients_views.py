from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum, F

from crm.models import Client, ServiceRequest
from crm.views import staff_required
from crm.permissions import ElementPermission
from crm.responses import json_response


class BaseClientView(ElementPermission):
    def get_client(self, request, request_method: str, with_service_requests_count: bool = False):
        """
        Получает клиента по client_id и проверяет доступ менеджера.
        """
        client_id = None

        if request_method == "GET":
            client_id = request.GET.get('client_id')
        elif request_method == "POST":
            client_id = request.POST.get('client_id')

        if not client_id:
            return json_response.validation_error("Expected client_id")

        try:
            if with_service_requests_count:
                client = Client.objects.annotate(
                    service_request_count=Count("service_requests")
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
            with_service_requests_count=True
        )

        # Если вместо объекта вернулся json, то возвращаем его клиенту
        if isinstance(client, JsonResponse):
            return client

        # Ожидаемая прибыль по всем заявкам клиента
        total_profit = (ServiceRequest.objects.filter(
            client=client
        )
        .annotate(
            profit=F("total_price") - F("cost_price")
        ).aggregate(
            total_profit=Sum("profit")
        ))["total_profit"] or 0

        context = {
            "client": client,
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

        new_name = data.get("ClientName")
        new_phone = data.get("ClientPhone")
        new_whatsapp = data.get("ClientWhatsapp")
        new_telegram = data.get("ClientTelegram")
        new_email = data.get("ClientEmail")

        client.name = new_name
        client.phone = new_phone
        client.whatsapp = new_whatsapp
        client.telegram = new_telegram
        client.email = new_email
        client.save()

        return JsonResponse({
            "success": True
        })