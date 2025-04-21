from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from api.serializers import ReminderSerializer
from crm.models import Reminder

class ReminderViewSet(ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    http_method_names = ["delete", "get"]

    # TODO: Добавить permission_class

    def destroy(self, request, *args, **kwargs):
        """
        Ожидает метод delete и параметр /id/.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
