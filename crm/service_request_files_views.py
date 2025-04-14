from django.utils.decorators import method_decorator
from django.views import View

from crm.views import staff_required


class ServiceRequestFilesBaseView:
    pass

@method_decorator(staff_required, "dispatch")
class ServiceRequestFilesAddView(ServiceRequestFilesBaseView, View):
    """
    Добавление новых файлов для ServiceRequest
    """
    def get(self, request):
        """
        Получение окна с формой для создания нового файла для ServiceRequest
        """
        # Получить id объекта ServiceRequest.
        # Проверить наличие объекта ServiceRequest.
        # Проверить доступность объекта ServiceRequest для менеджера.
        # Проверить тип файлов (image | document) для контекста
        pass

    def post(self, request):
        # Получить id объекта ServiceRequest.
        # Проверить наличие объекта ServiceRequest.
        # Проверить доступность объекта ServiceRequest для менеджера.
        # Проверить тип файлов (image | document) для определения логики сохранения (ServiceRequestImage или ServiceRequestDocument)
        # Распарсить и сохранить.
        pass

