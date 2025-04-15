from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View

from crm.models import ServiceRequest
from crm.views import staff_required


class ServiceRequestFilesBaseView:
    pass

@method_decorator(staff_required, "dispatch")
class ServiceRequestFilesListView(View):
    """
    Страница с документами и изображениями для ServiceRequest
    """
    def get(self, request, service_request_id, filter_by=None):
        try:
            service_request = ServiceRequest.objects.prefetch_related(
                "images",
                "documents"
            ).get(id=service_request_id)
        except ServiceRequest.DoesNotExist:
            return HttpResponse("ServiceRequest not found", status=404)

        context = {
            "images": service_request.images.all(),
            "documents": service_request.documents.all(),
            "service_request": service_request
        }

        return render(
            request,
            template_name="crm/files-for-service-request/files-gallery-for-service-request.html",
            context=context
        )

@method_decorator(staff_required, "dispatch")
class ServiceRequestFilesAddView(ServiceRequestFilesBaseView, View):
    """
    Добавление новых файлов для ServiceRequest
    """
    def get(self, request):
        """
        Получение окна с формой для создания нового файла для ServiceRequest
        """
        service_request_id = request.GET.get("service_request_id")
        files_type = request.GET.get("files_type")
        # Получить id объекта ServiceRequest.
        # Проверить наличие объекта ServiceRequest.
        # Проверить доступность объекта ServiceRequest для менеджера.
        # Проверить тип файлов (images | documents) для контекста
        context = {
            "files_type": files_type
        }
        new_content = render_to_string(
            request=request,
            template_name="crm/files-for-service-request/add-item-modal.html",
            context=context
        )
        return JsonResponse({
            "success": True,
            "new_content": new_content
        })

    def post(self, request):
        # Получить id объекта ServiceRequest.
        # Проверить наличие объекта ServiceRequest.
        # Проверить доступность объекта ServiceRequest для менеджера.
        # Проверить тип файлов (image | document) для определения логики сохранения (ServiceRequestImage или ServiceRequestDocument)
        # Распарсить и сохранить.
        pass

