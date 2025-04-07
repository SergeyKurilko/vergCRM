from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from crm.models import DisplayNotification
from crm.responses import JsonResponses as json_response



class GetDisplayNotification(View):
    def get(self, request):
        """
        Принимает ajax-request, проверяет наличие DisplayNotification для
        пользователя. Возвращает JsonResponse с html для отображения на экране оповещения.
        Arguments:
             request (WSGIRequest): объект запроса WSGIRequest
        Return:
            JsonResponse (JsonResponse): JsonResponse с html
        """
        if not request.user.is_authenticated:
            return json_response.validation_error(
                "User not authenticated"
            )

        notifications = DisplayNotification.objects.filter(
            user=request.user,
            viewed=False
        )

        # Устанавливаем интервал в сессии
        interval = 5000 if notifications.exists() else 30000
        request.session['notification_check_interval'] = interval

        if not notifications.exists():
            return JsonResponse({"success": True, "interval": interval})

        notification = notifications.first()

        context = {
            "notification_header": "Напоминание" if notification.type == "reminder" else "Оповещение",
            "message": notification.message,
            "notification_id": notification.id
        }

        html = render_to_string(
            template_name="crm/display_notifications/display_notification_card.html",
            context=context,
            request=request
        )

        return JsonResponse({
            "success": True,
            "notification": html,
            "interval": interval,
            "notification_id": notification.id
        })


class MarkNotificationAsRead(View):
    """
    Сделать DisplayNotification прочитанным (viewed=True)
    """
    def post(self, request):
        notification = get_object_or_404(
            DisplayNotification,
            id=request.POST.get('notification_id'),
            user=request.user
        )
        notification.viewed = True
        notification.save()
        return JsonResponse({"success": True})

