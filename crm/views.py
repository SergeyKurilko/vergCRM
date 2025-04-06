from pprint import pprint
from django.db.models import F, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from functools import wraps
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator


from crm.models import ServiceRequest, Service, Client

def staff_required(view_func):
    """
    Декоратор для проверки, является ли пользователь is_staff
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('crm:login_page')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class CrmLoginView(View):
    def get(self, request):
        # Если пользователь уже в системе, то перенаправляем в dashboard
        if request.user.is_staff:
            return redirect(reverse("crm:dashboard"))
        return render(request, "crm/login_page.html")

    def post(self, request):
        user_data = request.POST
        username = user_data.get('Username')
        password = user_data.get('Password')
        if not username or not password:
            return JsonResponse({
                "error": True,
                "message": "Bad request"
            }, status=400)
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({
                "error": True,
                "message": "Неправильный логин или пароль"
            }, status=400)
        login(request, user)
        # Возвращаем успешный ответ с HTTP статусом 200 (OK)
        return JsonResponse({
            "success": True,
            "message": "Login successful",
            "redirect_url": reverse("crm:dashboard")
        })


def test(request):
    from telegram_bot.bot import bot
    st = request.user.is_staff
    manager_id = request.user.userprofile.telegram_id
    bot.send_message(
        chat_id=manager_id,
        text="Привет. Это тестовое сообщение из джанго"
    )
    return HttpResponse(f"user.is_staff: {st}")


def user_logout_view(request):
    """
    Выход пользователя из системы
    """
    logout(request)
    return redirect(reverse("crm:login_page"))


@method_decorator(staff_required, name='dispatch')
class DashboardView(View):
    def get(self, request):

        # Извлекаем все заявки менеджера
        my_active_service_requests = ServiceRequest.objects.filter(
            manager=request.user,
            status__in={"new", "in_progress"}
        )

        active_requests_count = my_active_service_requests.count()
        total_expected_profit = (
            my_active_service_requests
            .annotate(difference=F('total_price') - F('cost_price'))
            .aggregate(total_expected_profit=Sum('difference'))
            .get('total_expected_profit', None)
        )

        context = {
            "active_requests_count": active_requests_count,
            "total_expected_profit": total_expected_profit
        }
        return render(request, "crm/dashboard.html", context)


@method_decorator(staff_required, name='dispatch')
class ServiceRequestsListView(View):
    def get(self, request):
        service_requests = ServiceRequest.objects.filter(
            manager=request.user
        ).annotate(expected_profit=F('total_price') - F('cost_price'))

        # Проверяем фильтр status
        allowed_statuses = {"in_progress", "completed", "canceled", "all"}
        status =  request.GET.get("status")
        humanized_status_title = None
        if status and status != 'all' and status in allowed_statuses:
            service_requests = service_requests.filter(status=status)
            humanized_status_title = dict(ServiceRequest.STATUS_CHOICES).get(status)


        # Получаем количество service_requests
        service_requests_quantity = service_requests.count()


        # Пагинация
        paginator = Paginator(service_requests, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "service_requests": page_obj,
            "current_status": status,
            "service_requests_quantity": service_requests_quantity,
            "humanized_status_title": humanized_status_title
        }

        return render(request, "crm/service_requests_list.html", context)


@method_decorator(staff_required, name='dispatch')
class ServiceRequestCreateView(View):
    def get(self, request):
        service_list = Service.objects.all()
        client_list = Client.objects.filter(manager=request.user)

        context = {
            "service_list": service_list,
            "client_list": client_list
        }

        return render(request, "crm/add_service_request.html", context)


@method_decorator(staff_required, "dispatch")
class ServiceRequestDetailView(View):
    def get(self, request, service_request_id):
        service_request = get_object_or_404(
            ServiceRequest, id=service_request_id
        )
        if service_request.manager != request.user:
            return redirect(reverse("crm:dashboard"))


        profit = f"{str(service_request.total_price - service_request.cost_price)} ₽"

        context = {
            "service_request": service_request,
            "profit": profit,
        }
        return render(request, "crm/service_request_detail.html", context)









