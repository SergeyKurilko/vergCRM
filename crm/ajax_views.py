from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpRequest
from django.db import models
from django.views import View
from datetime import datetime
from crm.permissions import ElementPermission



from crm.views import staff_required
from crm.models import (Service, Client, ServiceRequest,
                        NoteForServiceRequest, CostPriceCase,
                        PartOfCostPriceCase, Task)


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

    @staticmethod
    def manager_forbidden(message: str):
        return JsonResponse({
            "error": True,
            "message": message
        }, status=403)

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
class DeleteServiceRequest(ElementPermission, View):
    """Удаление заявки"""
    def get(self, request):
        """Получение окна подтверждения удаления заявки"""
        service_request_id = request.GET.get("service_request_id")
        if not service_request_id:
            return json_response.validation_error(
                "Ожидается номер заявки."
            )

        try:
            service_request = ServiceRequest.objects.get(id=service_request_id)
        except ServiceRequest.DoesNotExist:
            return json_response.not_found_error(
                "Заявка не найдена"
            )

        if not self.verification_owner(request, service_request):
            return json_response.manager_forbidden(
                "Verification error"
            )
        context =  {
            "service_request": service_request
        }

        confirm_delete_modal = render_to_string(
            template_name="crm/incl/confirm-delete-service-request.html",
            request=request,
            context=context
        )

        return JsonResponse({
            "success": True,
            "confirm_delete_modal": confirm_delete_modal
        })

    def post(self, request):
        """Подтверждение удаления заявки"""
        service_request_id = request.POST.get("delete_service_request")
        # Проверка тела на наличие service_request_id
        if not service_request_id:
            return json_response.validation_error(
                "Ожидается номер заявки."
            )

        # Поиск заявки в БД
        try:
            service_request = ServiceRequest.objects.get(id=service_request_id)
        except ServiceRequest.DoesNotExist:
            return json_response.not_found_error(
                "Заявка не найдена"
            )

        # Проверка прав на удаление
        if not self.verification_owner(request, service_request):
            return json_response.manager_forbidden(
                "Verification error"
            )

        # service_request.delete()

        # После удаления отправляем в скрипт ссылку на перенаправление к списку задач
        return JsonResponse({
            "success": True,
            "url_for_redirect": reverse("crm:service_requests_list")
        })

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
class AjaxChangeTotalPriceForServiceRequest(ElementPermission, View):
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

        # Поиск заявки
        try:
            service_request = ServiceRequest.objects.get(id=service_id)
        except ServiceRequest.DoesNotExist:
            return json_response.not_found_error("Заявка не найдена")

        # Проверка прав менеджера на изменение заявки
        if not self.verification_owner(request, service_request):
            return json_response.manager_forbidden(
                "Verification error"
            )

        new_profit = int(new_total_price) - service_request.cost_price

        service_request.total_price = new_total_price
        service_request.save()


        return JsonResponse({
            "success": True,
            "new_total_price": f"{new_total_price} ₽",
            "new_profit": f"{new_profit} ₽"
        }, status=200)


@method_decorator(staff_required, "dispatch")
class GetHtmlForCalculateCostPrice(View):
    def get(self, request):
        allowed_queries_params = {'get_cases', 'add_case'}
        query_param = request.GET.get("query_param")
        #TODO: обработать ответ с неразрешенным параметром или с отсутствием параметра

        # Получение html для рендера содержимого calculate-cost-price-offcanvas.html
        if query_param == 'get_cases':
            service_request_id = request.GET.get("ServiceRequestId")
            cost_price_cases = CostPriceCase.objects.filter(
                service_request_id=service_request_id
            )
            context = {
                "test": "Привет!",
                "cost_price_cases": cost_price_cases,
                "service_request_id": service_request_id
            }
            offcanvas_html = render_to_string(
                template_name="crm/incl/calculate-cost-price-offcanvas.html",
                request=request,
                context=context
            )
            return JsonResponse({
                "success": True,
                "offcanvas_html": offcanvas_html
                }
            )

        # Получение html для рендера формы создания нового CostPriceCase
        if query_param == 'add_case':
            service_request_id = request.GET.get("ServiceRequestId")
            context = {
                "service_request_id": service_request_id
            }
            add_cost_case_html = render_to_string(
                template_name="crm/incl/add-cost-price-case-form.html",
                request=request,
                context=context
            )

            return JsonResponse({
                "success": True,
                "add_cost_case_html": add_cost_case_html
                }
            )


@method_decorator(staff_required, "dispatch")
class UpdateListOfCostPriceCases(View):
    def get(self, request: HttpRequest):

        service_request_id = request.GET.get("ServiceRequestId")
        cost_price_cases = CostPriceCase.objects.filter(
            service_request_id=service_request_id
        )
        context = {
            "cost_price_cases": cost_price_cases,
            "service_request_id": service_request_id
        }
        list_of_cost_prices_html = render_to_string(
            template_name="crm/dynamic_content/calculate-cost-content.html",
            request=request,
            context=context
        )
        return JsonResponse({
            "success": True,
            "new_content": list_of_cost_prices_html
            }
        )


@method_decorator(staff_required, "dispatch")
class AddCostPriceCaseView(View):
    def post(self, request):
        data = request.POST

        case_title = data.get("case_title")
        service_request_id = data.get("service_request")
        total_cost_price = data.get("total_cost_price")

        # Создаем объект CostPriceCase
        cost_price_case = CostPriceCase.objects.create(
            title=case_title,
            service_request_id=service_request_id,
            sum=int(total_cost_price)
        )

        # Парсим данные из формы для создания списка PartOfCostPriceCase объектов
        cost_price_parts = []
        for key, value in data.items():
            if key.startswith("part_title_"):
                index = key.split("_")[-1]
                part_title = value
                part_price = data.get(f"part_price_{index}")


                if part_title and part_price:
                    cost_price_parts.append(
                        PartOfCostPriceCase(
                            title=part_title,
                            sum=int(part_price),
                            cost_price_case=cost_price_case
                        )
                    )

        # Создаем все PartOfCostPriceCase за один запрос
        PartOfCostPriceCase.objects.bulk_create(cost_price_parts)

        return JsonResponse({
            "success": True,
            "case_title": case_title,
            "case_price": total_cost_price,
            "cost_price_case_id": cost_price_case.id,
            "service_request_id": service_request_id,
            "url_for_update_cost_price_list": reverse(
                "crm:ajax-update-list-cost-prices"
                )
            })


@method_decorator(staff_required, "dispatch")
class ChangeCurrentCostCaseView(View):
    def post(self, request):
        request_id = request.POST.get("request_id")
        case_id = request.POST.get("case_id")

        cost_price_case = CostPriceCase.objects.get(id=case_id)
        cost_price_case.current = True
        cost_price_case.save()

        ServiceRequest.objects.filter(id=request_id).update(cost_price=cost_price_case.sum)

        (CostPriceCase.objects.filter(
            service_request_id=request_id
        )
        .exclude(id=case_id)
        .update(current=False))

        return JsonResponse({
            "success": True,
            "url_for_update_cost_price_list": reverse(
                "crm:ajax-update-list-cost-prices"
            ),
            "current_cost_price": cost_price_case.sum
        })


@method_decorator(staff_required, "dispatch")
class DeleteCostCaseView(View):
    def get(self, request):
        case_id = request.GET.get("case_id")
        if not case_id:
            return json_response.validation_error("Expected case_id.")

        try:
            cost_price_case = CostPriceCase.objects.get(
                id=case_id
            )
        except CostPriceCase.DoesNotExist:
            return json_response.not_found_error("CostPriceCase not found.")

        if cost_price_case.current:
            return json_response.validation_error("Нельзя удалить выбранный кейс.")

        context = {
            "case_id": cost_price_case.id,
            "case_title": cost_price_case.title,
            "case_sum": cost_price_case.sum
        }
        confirm_delete_case_modal_html = render_to_string(
            template_name="crm/incl/confirm-delete-cost-price-case.html",
            request=request,
            context=context
        )

        return JsonResponse({
            "success": True,
            "confirm_delete_case_modal_html": confirm_delete_case_modal_html
        })

    def delete(self, request):
        case_id = request.GET.get("delete_case")
        if not case_id:
            return json_response.validation_error("Expected case_id.")

        try:
            cost_price_case = CostPriceCase.objects.get(
                id=case_id
            )
        except CostPriceCase.DoesNotExist:
            return json_response.not_found_error("CostPriceCase not found.")

        if cost_price_case.current:
            return json_response.validation_error("Нельзя удалить выбранный кейс.")

        cost_price_case.delete()

        return JsonResponse({
            "success": True,
        })


@method_decorator(staff_required, "dispatch")
class CostPriceCaseDetailView(View):
    def get(self, request):
        case_id = request.GET.get("case_id")
        if not case_id:
            return json_response.validation_error("Expected case_id.")
        try:
            cost_price_case = CostPriceCase.objects.get(
                id=case_id
            )
        except CostPriceCase.DoesNotExist:
            return json_response.not_found_error("CostPriceCase not found.")

        cost_price_case_html = render_to_string(
            template_name='crm/incl/cost-price-case-detail-modal.html',
            context={"cost_price_case": cost_price_case},
            request=request,
        )

        return JsonResponse({
            "cost_price_case_html": cost_price_case_html
        })

        # # TODO: после завершения разработки поменять на json + render_to_string
        # return render(request,
        #               'crm/incl/cost-price-case-detail-modal.html',
        #               {"cost_price_case": cost_price_case})

    def post(self, request):
        """
        Редактирование кейса
        """
        query_dict = request.POST

        # Ожидаемые ключи
        required_keys = {'case_title', 'cost_price_id',
                         'total_cost_price',
                         'existing_parts_have_been_modified',
                         'total_price_has_been_changed',
                         'has_new_parts', 'case_title', 'for_delete_ids'}

        # Проверка наличия всех ожидаемых ключей в request.POST
        if not required_keys.issubset(set(query_dict.keys())):
            return json_response.validation_error(
                message="Что-то пошло не так. Перезагрузите страницу"
            )

        existing_parts_have_been_modified = query_dict.get("existing_parts_have_been_modified")
        cost_price_id = query_dict.get("cost_price_id")
        total_cost_price = query_dict.get("total_cost_price")
        total_price_has_been_changed = query_dict.get("total_price_has_been_changed")
        has_new_parts = query_dict.get("has_new_parts")
        for_delete_ids = query_dict.get("for_delete_ids")

        try:
            cost_price_case = CostPriceCase.objects.get(id=cost_price_id)
        except CostPriceCase.DoesNotExist:
            return json_response.not_found_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        # Проверка списка помеченных на удаление PartOfCostPriceCase и их удаление
        if len(for_delete_ids) > 0:
            PartOfCostPriceCase.objects.filter(
                id__in=for_delete_ids.split(',')
            ).delete()

        # Проверка флага изменения общей стоимости для ServiceRequest и CostPriceCase
        if total_price_has_been_changed == "true":
            cost_price_case.sum = int(total_cost_price)
            ServiceRequest.objects.filter(
                id=cost_price_case.service_request_id
            ).update(cost_price=int(total_cost_price))


        # Были изменены существующие поля
        if existing_parts_have_been_modified == "true":
            modified_parts_ids = []
            for key, value in query_dict.items():
                if key.startswith("part_title_"):
                    index = key[11:]
                    modified_parts_ids.append(index)

            # Список объектов для обновления
            modified_parts = PartOfCostPriceCase.objects.filter(
                id__in=modified_parts_ids
            )

            # Обновляем значения в полях title и price у измененных PartOfCostPriceCase
            for part in modified_parts:
                part_id = part.id
                part.title = query_dict[f"part_title_{part_id}"]
                part.sum = int(query_dict[f"part_price_{part_id}"])

            PartOfCostPriceCase.objects.bulk_update(modified_parts, ['title', 'sum'])

        # Были добавлены новые поля (новые PartOfCostPriceCase)
        if has_new_parts == "true":
            new_parts = []
            for key, value in query_dict.items():
                if key.startswith("new_part_title_"):
                    index = key[15:]
                    new_part = PartOfCostPriceCase(
                            title=query_dict[f"new_part_title_{index}"],
                            sum=int(query_dict[f"new_part_price_{index}"]),
                            cost_price_case=cost_price_case,
                        )
                    new_parts.append(new_part)


            # Создаем все PartOfCostPriceCase за один запрос
            PartOfCostPriceCase.objects.bulk_create(new_parts)

        if cost_price_case.title != query_dict["case_title"]:
            cost_price_case.title = query_dict["case_title"]

        cost_price_case.save()

        return JsonResponse(
            {
                "success": True,
                "case_id": cost_price_case.id,
                "url_for_update_cost_price_list": reverse(
                    "crm:ajax-update-list-cost-prices"
                ),
                "case_is_current": cost_price_case.current,
                "current_cost_price": cost_price_case.sum
            }
        )


@method_decorator(staff_required, "dispatch")
class GetTaskListForServiceRequest(View):
    """Получение списка задач"""
    def get(self, request: HttpRequest) -> JsonResponse:
        service_request_id = request.GET.get("service_request_id")
        filter_by = request.GET.get("filter_by")

        # Проверка номера заявки (в любом сценарии)
        if not service_request_id:
            return json_response.validation_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        # Поиск объекта ServiceRequest
        try:
            service_request = ServiceRequest.objects.get(
                id=service_request_id
            )
        except ServiceRequest.DoesNotExist:
            return json_response.not_found_error(
                "Заявка не найдена"
            )

        # Если в параметрах запроса нет фильтра
        if not filter_by:
            # Получение списка задач для заявки без фильтров (основной список)
            tasks = service_request.tasks.all().exclude(is_completed=True)
            context = {
                "tasks": tasks,
                "filtered_query": False
            }

            # Контент для добавления нового offcanvas со списком задач
            offcanvas_with_all_tasks_html = render_to_string(
                template_name="crm/incl/tasks-list-for-request-offcanvas.html",
                request=request,
                context=context
            )
            return JsonResponse({
                "success": True,
                "offcanvas_with_all_tasks_html": offcanvas_with_all_tasks_html,
            })

        # Если в параметрах запроса есть фильтр
        else:
            # Получение списка с фильтрацией
            allowed_filters = {'all', 'expired',  'is_completed'}

            # Проверка допустимого параметра фильтрации
            if filter_by not in allowed_filters:
                return json_response.validation_error(
                    "Недопустимый фильтр"
                )
            else:
                if filter_by != 'all':
                    # Формируем словарь фильрации
                    filter_dict = {filter_by: True}
                    tasks = service_request.tasks.filter(
                        **filter_dict
                    )
                else:
                    tasks = service_request.tasks.all()

                context = {
                    "tasks": tasks,
                    "filtered_by": filter_by,
                    "filtered_query": True
                }

                # Формирование контента для замены в offcanvas со списком задач
                tasks_html_for_update = render_to_string(
                    template_name="crm/dynamic_content/update-task-list-for-request.html",
                    context=context,
                    request=request
                )

                return JsonResponse({
                    "success": True,
                    "new_content": tasks_html_for_update,
                })

@method_decorator(staff_required, name="dispatch")
class AddNewTaskForServiceRequest(View):
    def get(self, request):
        """Получение окна для создания новой задачи"""
        service_request_id = request.GET.get("service_request_id")

        if not service_request_id:
            return json_response.validation_error(
                "Некорректный запрос"
            )
        if ServiceRequest.objects.filter(id=service_request_id).exists():
            context = {
                "manager_id": request.user.id,
                "service_request_id": service_request_id
            }
            new_content = render_to_string(
                    template_name="crm/incl/modal-for-add-new-task-for-request.html",
                    context=context,
                    request=request
            )
            return JsonResponse({
                "success": True,
                "new_content": new_content
            })

    def post(self, request):
        """Создание новой задачи для заявки"""
        data = request.POST
        required_fields = {
            "manager_id", "service_request_id",
            "title", "text", "must_be_completed_by"
        }
        # Проверка наличия всех обязательных полей
        if not required_fields.issubset(set(data.keys())):
            return json_response.validation_error(
                message="Что-то пошло не так. Перезагрузите страницу"
            )

        # Извлечение данных из тела запроса
        manager_id = data.get("manager_id")
        service_request_id = data.get("service_request_id")
        title = data.get("title")
        text = data.get("text")
        must_be_completed_by = data.get("must_be_completed_by")
        reminder = data.get("reminder")

        if not manager_id or not service_request_id:
            return json_response.validation_error(
                "Expected manager_id and service_request_id"
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
        task_reminder = True if reminder else False

        new_task = Task.objects.create(
            title=title,
            text=text,
            service_request_id=service_request_id,
            manager_id=manager_id,
            must_be_completed_by=must_be_completed_by,
            reminder=task_reminder
        )

        return JsonResponse({
            "success": True,
            "url_for_update_content": reverse("crm:task_list_for_request")
        })


@method_decorator(staff_required, name="dispatch")
class TaskForRequestDetailView(View):
    def get(self, request):
        """Получение модального окна с детальным описанием задачи"""
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

        context = {
            "task": task
        }

        new_content = render_to_string(
            template_name="crm/incl/modal-for-task-for-request-detail.html",
            context=context,
            request=request
        )
        return JsonResponse({
            "success": True,
            "new_content": new_content
        })

    def post(self, request: HttpRequest):
        data = request.POST
        print(data)
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
        reminder = data.get("reminder")

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
        task_reminder = True if reminder else False

        task.title=title
        task.text=text
        task.must_be_completed_by=must_be_completed_by
        task.reminder=task_reminder

        task.save()

        return JsonResponse({
            "success": True,
            "url_for_update_content": reverse("crm:task_list_for_request")
        })

class DeleteTaskForRequestView(View):
    def get(self, request):
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
            template_name="crm/incl/confirm-delete-task.html",
            request=request,
            context=context
        )

        return JsonResponse({
            "success": True,
            "new_content": new_content
        })

    def post(self, request):
        task_id = request.POST.get("delete_task_id")
        if not task_id:
            print("Нет параметра delete_task_id")
            return json_response.validation_error(
                "Что-то пошло не так. Перезагрузите страницу."
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            print("Не найдена задача")
            return json_response.not_found_error(
                "Задача не найдена"
            )

        if request.user.id != task.manager.id:
            print("Задача не принадлежит менеджеру")
            return json_response.manager_forbidden(
                "Задача не принадлежит менеджеру"
            )

        task.delete()

        return JsonResponse({
            "success": True,
            "url_for_update_content": reverse("crm:task_list_for_request")
        })
