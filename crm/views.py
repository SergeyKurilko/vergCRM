

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


def check_access_rights(user: User):
    return user.is_staff


def main(request):
    if check_access_rights(request.user):
        return redirect(reverse("crm:dashboard"))
    else:
        return redirect('crm:login_page')


class CrmLoginView(View):
    def get(self, request):
        if check_access_rights(request.user):
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
            "redirect_url": reverse("crm:main")
        })


class DashboardView(View):
    def get(self, request):
        if check_access_rights(request.user):
            return render(request, "crm/dashboard.html")
        else:
            return redirect(reverse('crm:login_page'))


def test(request):
    st = request.user.is_staff
    return HttpResponse(f"user.is_staff: {st}")



