from django.db.models import F, Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from crm.models import ServiceRequest
from functools import wraps
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

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



def check_access_rights(user: User):
    print("Проверка пользователя")
    print(f"not user.is_staff: {not user.is_staff}")
    print(f"not user.is_authenticated: {not user.is_authenticated}")
    if not user.is_staff or not user.is_authenticated:
        print("Все условия сработали")
        return redirect('crm:login_page')



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
    # Тестовая view
    st = request.user.is_staff
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

        # Пагинация
        paginator = Paginator(service_requests, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.page(page_number)

        context = {
            "service_requests": page_obj
        }

        return render(request, "crm/service_requests_list.html", context)






