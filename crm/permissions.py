from django.http import HttpRequest

class ElementPermission:
    """
    Проверка доступа менеджера к объекту.
    """
    @staticmethod
    def verification_owner(request: HttpRequest, obj):
        """
        Проверка прав менеджера на CRUD объекта
        """
        user_id = request.user.id
        owner_id = obj.manager.id
        return user_id == owner_id