from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View

from crm.models import ServiceRequest, ServiceRequestDocument, ServiceRequestImage
from crm.views import staff_required
from crm.responses import json_response


class ServiceRequestFilesBaseView:
    @staticmethod
    def validate_file_size(value):
        """Проверяет, что размер файла не более 10 мб"""
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            return json_response.validation_error(
                f"Размер файла ({value}) должен быть не более 10мб."
            )

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
            "files_type": files_type,
            "service_request_id": service_request_id
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
        service_request_id = request.POST.get("service_request_id")

        # TODO: проверить, есть ли такой service_request и есть ли права на него
        service_request = ServiceRequest.objects.get(id=service_request_id)
        files_type = request.POST.get("files_type")
        files = request.FILES
        actual_files_list_htm = None
        new_files = []
        if len(files) > 0:
            for key, value in files.items():
                # TODO: проверить форматы файлов

                # Проверка размера файла
                size_validate = self.validate_file_size(value)
                if isinstance(size_validate, JsonResponse):
                    return size_validate
                if key.startswith("file"):
                    file = ServiceRequestDocument(
                        file=value,
                        service_request=service_request
                    )
                    new_files.append(file)

            if files_type == "documents":
                ServiceRequestDocument.objects.bulk_create(new_files)
                actual_files_list_htm = render_to_string(
                    template_name=
                    "crm/files-for-service-request/dynamic_content/actual-documents-list.html",
                    request=request,
                    context={
                        "documents": ServiceRequestDocument.objects.filter(
                            service_request=service_request
                        )
                    }
                )
            elif files_type == "images":
                ServiceRequestImage.objects.bulk_create(new_files)
                actual_files_list_htm = render_to_string(
                    template_name=
                    "crm/files-for-service-request/dynamic_content/actual-images-list.html",
                    request=request,
                    context={
                        "images": ServiceRequestImage.objects.filter(
                            service_request=service_request
                        )
                    }
                )

        return JsonResponse({
            "success": True,
            "actual_files_list_htm": actual_files_list_htm,
            "files_type": files_type
        })
