from rest_framework.serializers import ModelSerializer
from crm.models import Reminder


class ReminderSerializer(ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = (
            'task', 'mode', 'scheduled_datetime',
            'recurring_days', 'recurring_time',
            'last_reminder_sent'
        )
