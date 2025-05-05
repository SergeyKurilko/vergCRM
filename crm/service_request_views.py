from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View

from crm.json_responses import JsonResponses as json_response
from crm.views import staff_required
from crm.models import ServiceRequest


class ServiceRequestBaseView:
    def check_service_request_exitst(self, service_request_id):
        return (ServiceRequest.objects
                .filter(id=service_request_id)
                .exists())

    def check_access_and_get_request(self, request, service_request_id):
        """Проверка доступа к заявке для пользователя"""

        # Проверка существования заявки
        if not self.check_service_request_exitst(service_request_id):
            return json_response.not_found_error(
                "Service request not found"
            )

        service_request = (
            ServiceRequest
           .objects
           .prefetch_related('tasks')
           .get(id=service_request_id)
        )

        if service_request.manager.id != request.user.id:
            return json_response.manager_forbidden(
                "Нет доступа к заявке"
            )

        return service_request


@method_decorator(staff_required, "dispatch")
class ServiceRequestCompleteView(ServiceRequestBaseView, View):
    """Завершение заявки"""
    def get(self, request):
        """
        Получение модального окна для подтверждения завершения заявки.
        """
        service_request_id = request.GET.get("service_request_id")
        if not service_request_id or not service_request_id.isdigit():
            return json_response.validation_error(
                "Expected service request id"
            )

        service_request = self.check_access_and_get_request(
            request, service_request_id
        )

        if isinstance(service_request, JsonResponse):
            return service_request

        context = {
            "service_request": service_request
        }

        new_content = render_to_string(
            request=request,
            template_name="crm/incl/confirm-complete-service-request.html",
            context=context
        )

        return JsonResponse({
            "success": True,
            "new_content": new_content
        })

    def post(self, request):
        """
        Подтверждение завершения заявки.
        """
        service_request_id = request.POST.get("service_request_id")
        if not service_request_id or not service_request_id.isdigit():
            return json_response.validation_error(
                "Expected service request id"
            )

        service_request = self.check_access_and_get_request(
            request, service_request_id
        )

        if isinstance(service_request, JsonResponse):
            return service_request

        for task in service_request.tasks.all():
            task.delete()

        service_request.status = 'completed'
        service_request.save()

        return JsonResponse({
            "success": True
        })