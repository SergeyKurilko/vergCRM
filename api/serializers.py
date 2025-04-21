from rest_framework.serializers import ModelSerializer
from crm.models import Reminder, Task


class ReminderSerializer(ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = (
            'task', 'mode', 'scheduled_datetime',
            'recurring_days', 'recurring_time',
            'last_reminder_sent'
        )


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
