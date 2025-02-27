import os

def service_request_image_path(instance, filename):
    """
    Генерация пути для хранения ImageForServiceRequest
    """
    return os.path.join('images/', str(instance.service_request.id), filename)