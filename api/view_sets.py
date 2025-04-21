from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from datetime import datetime, timedelta
from django.utils import timezone


from api.serializers import ReminderSerializer, TaskSerializer
from api.permissions import HasApiSecretKey, IsReminderOwner

from crm.models import Reminder, Task

class ReminderViewSet(ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    http_method_names = ["delete", "get"]

    permission_classes = [HasApiSecretKey, IsReminderOwner]

    def destroy(self, request, *args, **kwargs):
        """
        Ожидает метод delete и параметр /id/.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ["patch", "get"]

    @action(methods=["patch"], detail=True, url_path="postpone/hour")
    def postpone_one_hour(self, request, pk=None):
        """Перенос срока задачи на час вперед"""
        task = self.get_object()
        new_must_be_completed_by = task.must_be_completed_by + timedelta(hours=1)
        task.must_be_completed_by = new_must_be_completed_by
        if task.expired:
            now = timezone.make_aware(datetime.now()) # добавляем текущую временную зону к now
            if new_must_be_completed_by > now:
                task.expired = False
        task.save()
        return Response(
            self.get_serializer(task).data,
            status=status.HTTP_200_OK
        )

    @action(methods=["patch"], detail=True, url_path="postpone/three_hour")
    def postpone_three_hour(self, request, pk=None):
        """Перенос срока задачи на три часа вперед"""
        task = self.get_object()
        new_must_be_completed_by = task.must_be_completed_by + timedelta(hours=3)
        task.must_be_completed_by = new_must_be_completed_by
        task.before_one_hour_deadline_notification = False
        if task.expired:
            now = timezone.make_aware(datetime.now()) # добавляем текущую временную зону к now
            if new_must_be_completed_by > now:
                task.expired = False
        task.save()
        return Response(
            self.get_serializer(task).data,
            status=status.HTTP_200_OK
        )

    @action(methods=["patch"], detail=True, url_path="postpone/day")
    def postpone_one_day(self, request, pk=None):
        """Перенос срока задачи на день вперед"""
        task = self.get_object()
        new_must_be_completed_by = task.must_be_completed_by + timedelta(days=1)
        task.must_be_completed_by = new_must_be_completed_by
        task.before_one_hour_deadline_notification = False
        if task.expired:
            now = timezone.make_aware(datetime.now()) # добавляем текущую временную зону к now
            if new_must_be_completed_by > now:
                task.expired = False
        task.save()
        return Response(
            self.get_serializer(task).data,
            status=status.HTTP_200_OK
        )

    @action(methods=["patch"], detail=True, url_path="postpone/week")
    def postpone_one_week(self, request, pk=None):
        """Перенос срока задачи на неделю вперед"""
        task = self.get_object()
        new_must_be_completed_by = task.must_be_completed_by + timedelta(days=7)
        task.must_be_completed_by = new_must_be_completed_by
        task.before_one_hour_deadline_notification = False
        task.before_one_workday_deadline_notification = False
        if task.expired:
            now = timezone.make_aware(datetime.now()) # добавляем текущую временную зону к now
            if new_must_be_completed_by > now:
                task.expired = False
        task.save()
        return Response(
            self.get_serializer(task).data,
            status=status.HTTP_200_OK
        )




