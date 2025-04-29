from django.urls import path
from rest_framework.routers import DefaultRouter
from api.view_sets import ReminderViewSet, TaskViewSet
from api.views import check_telegram_access

router = DefaultRouter()
router.register(r'reminders', ReminderViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path("check_telegram_access/<str:telegram_id>/",
         check_telegram_access, name="check_telegram_access"),
    *router.urls
]