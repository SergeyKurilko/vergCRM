from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

from crm.json_responses import JsonResponses as json_response
from crm.views import staff_required
from crm.models import Reminder

@method_decorator(staff_required, "dispatch")
class GetContentForNewReminder(View):
    def get(self, request):
        """
        Отправляет контент для добавления
        нового напоминания для задачи
        """
        current_reminder_number = request.GET.get('reminder_number')
        context = {
            "current_reminder_number": current_reminder_number
        }
        new_reminder_card = render_to_string(
            template_name="crm/reminders/dynamic/card-for-add-reminder.html",
            request=request,
            context=context
        )
        return JsonResponse({
            "success": True,
            "new_reminder_card": new_reminder_card
        })


@method_decorator(staff_required, "dispatch")
class DeleteReminderView(View):
    def get(self, request):
        reminder_id = request.GET.get("reminder_id")
        if not reminder_id:
            return json_response.validation_error(
                message="Expected reminder id"
            )

        try:
            reminder = Reminder.objects.get(id=reminder_id)
        except Reminder.DoesNotExist:
            return json_response.not_found_error(
                "Reminder not found"
            )

        if reminder.task.manager != request.user:
            return json_response.manager_forbidden(
                "No access"
            )

        reminder.delete()
        return JsonResponse({
            "success": True
        })
