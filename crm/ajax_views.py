from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View

from crm.views import staff_required
from crm.models import Service, Client, ServiceRequest, NoteForServiceRequest


class JsonResponses:
    """
    Типовые ответы для ajax запросов с клиентской стороны.
    """
    @staticmethod
    def validation_error(message: str):
        return JsonResponse({
            "error": True,
            "message": message
        }, status=422)

    @staticmethod
    def not_found_error(message: str):
        return JsonResponse({
            "error": True,
            "message": message
        }, status=404)

json_response = JsonResponses()



@method_decorator(staff_required, "dispatch")
class AddNewServiceAjaxView(View):
    """
    Создание новой заявки
    """
    def post(self, request):
        service_name = request.POST.get("ServiceName")

        # Проверка наличия и длины названия услуги
        if not service_name or (len(service_name) <4 or len(service_name) > 350):
            return JsonResponse({
                "success": False,
                "message": "Название услуги должно быть от 4 до 350 символов."
            }, status=400)

        # Проверка наличия услуги в базе
        if Service.objects.filter(title=service_name).exists():
            return JsonResponse({
                "success": False,
                "message": "Такая услуга уже есть. Выбери из списка."
            }, status=400)

        # Создание новой услуги
        new_service = Service.objects.create(title=service_name)
        return JsonResponse({
            "success": True,
            "message": "Новая услуга создана",
            "new_service_title": new_service.title,
            "new_service_id": new_service.id
        }, status=201)


@method_decorator(staff_required, "dispatch")
class AddNewClientAjaxView(View):
    """
    Добавление нового клиента.
    """
    def post(self, request):
        client_name = request.POST.get("ClientName")
        client_phone = request.POST.get("ClientPhone")
        client_whatsapp = request.POST.get("ClientWhatsapp")
        client_telegram = request.POST.get("ClientTelegram")
        client_email = request.POST.get("ClientEmail")
        manager = request.user

        if not client_name or not client_phone:
            return JsonResponse({
                "success": False,
                "message": "Заполните имя и телефон."
            }, status=400)

        if Client.objects.filter(name=client_name):
            return JsonResponse({
                "success": False,
                "message": "Такой клиент уже есть. Выбери из списка."
            }, status=400)

        new_client = Client.objects.create(
            name=client_name,
            phone=client_phone,
            whatsapp=client_whatsapp,
            telegram=client_telegram,
            email=client_email,
            manager=manager
        )

        return JsonResponse({
            "success": True,
            "message": "Новый клиент создан.",
            "new_client_id": new_client.id,
            "new_client_name": new_client.name,
        }, status=201)


@method_decorator(staff_required, "dispatch")
class AddNewServiceRequestAjaxView(View):
    """
    Добавление новой услуги для заявки.
    """
    def post(self, request):
        data = request.POST
        service_id = data.get('service_id')
        client_id = data.get('client_id')
        description = data.get('request_description')

        # Валидация ожидаемых данных
        if not service_id:
            return json_response.validation_error("Услуга не выбрана.")
        if not client_id:
            return json_response.validation_error("Клиент не выбран.")
        if len(description) < 5:
            return json_response.validation_error("Введите описание заявки. Не менее 5 символов.")

        new_service_request = ServiceRequest.objects.create(
            client_id=client_id,
            description=description,
            manager=request.user,
            service_id=service_id,
        )

        return JsonResponse({
            "success": True,
            "redirect_url": new_service_request.get_absolute_url()
        }, status=201)


@method_decorator(staff_required, "dispatch")
class AddNewNoteAjaxView(View):
    """
    Добавление заметки для заявки
    """
    def post(self, request):
        note_text = request.POST.get("note_text")
        service_request_id = request.POST.get("service_request_id")
        if len(note_text) < 5:
            return json_response.validation_error("Введите текст заметки. Не менее 5 символов.")
        if not service_request_id:
            return json_response.validation_error("Что-то пошло не так. Попробуйте перезагрузить страницу.")

        new_note = NoteForServiceRequest.objects.create(
            text=note_text,
            service_request_id=service_request_id
        )

        return JsonResponse({
            "success": True,
            "new_note_id": new_note.id,
            "new_note_text": new_note.text,
            "new_note_created_at": new_note.created_at
        }, status=201)


@method_decorator(staff_required, "dispatch")
class AddAddressForServiceRequest(View):
    """
    Добавление адреса для заявки.
    """
    def post(self, request):
        address = request.POST.get('address')
        service_request_id = request.POST.get('service-request')

        if not address:
            return json_response.validation_error("Введите адрес. Не менее 5 символов.")

        if len(address) < 5:
            return json_response.validation_error("Введите адрес. Не менее 5 символов.")

        # Обновляем только поле address
        updated = ServiceRequest.objects.filter(pk=service_request_id).update(address=address)

        if not updated:
            return json_response.not_found_error("Заявка не найдена")


        return JsonResponse({
            "success": True,
            "address": address
        }, status=200)


@method_decorator(staff_required, "dispatch")
class AjaxChangeTotalPriceForServiceRequest(View):
    """
    Изменение общей стоимости для заявки.
    Ожидает ajax запрос из скрипта.
    """
    def post(self, request):
        new_total_price = request.POST.get("new_total_price")
        service_id = request.POST.get("service_id")

        if not new_total_price:
            return json_response.validation_error(
                message="Введите стоимость."
            )
        if not new_total_price.isdigit():
            return json_response.validation_error(
                message="Должно быть числом больше нуля."
            )

        try:
            service_request = ServiceRequest.objects.get(id=service_id)
        except ServiceRequest.DoesNotExist:
            return json_response.not_found_error("Заявка не найдена")

        new_profit = int(new_total_price) - service_request.cost_price

        service_request.total_price = new_total_price
        service_request.save()


        return JsonResponse({
            "success": True,
            "new_total_price": f"{new_total_price} ₽",
            "new_profit": f"{new_profit} ₽"
        }, status=200)