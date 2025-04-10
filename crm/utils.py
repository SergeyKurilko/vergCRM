import os

def service_request_file_path(instance, filename):
    """
    Генерация пути для хранения ImageForServiceRequest
    """
    return os.path.join('files/', str(instance.service_request.id), filename)