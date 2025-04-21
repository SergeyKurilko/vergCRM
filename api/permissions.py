from rest_framework import permissions
from django.conf import settings

class HasApiSecretKey(permissions.BasePermission):
    """
    Глобальный допуск к API. Запрос должен иметь секретный ключ в заголовке X-API-KEY.
    """
    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-KEY")
        return api_key == settings.X_API_KEY


class IsReminderOwner(permissions.BasePermission):
    """
    Проверка прав на доступ к Reminder
    """
    def has_object_permission(self, request, view, obj):
        telegram_id = request.headers.get("Telegram-ID")
        if not telegram_id:
            return False
        return str(obj.task.manager.userprofile.telegram_id) == telegram_id