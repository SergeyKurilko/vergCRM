from django.http import JsonResponse

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