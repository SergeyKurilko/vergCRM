from rest_framework.routers import DefaultRouter
from api.view_sets import ReminderViewSet

router = DefaultRouter()
router.register(r'reminders', ReminderViewSet)

urlpatterns = router.urls