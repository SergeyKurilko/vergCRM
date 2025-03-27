from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

from crm.views import staff_required

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