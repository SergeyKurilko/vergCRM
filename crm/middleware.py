from django.shortcuts import redirect
from django.urls import reverse


# TODO: этот middleware отключен. Доработать ситуации со входом и выходом
class StaffCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('crm:login_page'):
            return self.get_response(request)

        if not request.user.is_staff:
            return redirect('crm:login_page')

        response = self.get_response(request)
        return response