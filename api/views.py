
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from crm.models import UserProfile
from api.permissions import HasApiSecretKey

@api_view(["GET"])
@permission_classes([HasApiSecretKey])
def check_telegram_access(request, telegram_id):
    """Проверка наличия в базе пользователя телеграм"""
    try:
        user_profile = UserProfile.objects.get(
            telegram_id=telegram_id
        )
        return Response({
            "allowed": True,
        }, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({
            "allowed": False
        }, status=status.HTTP_404_NOT_FOUND)