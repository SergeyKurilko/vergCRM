from rest_framework.routers import DefaultRouter
from api.view_sets import ReminderViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'reminders', ReminderViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = router.urls