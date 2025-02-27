from django.urls import path
from crm.views import main, CrmLoginView, DashboardView, test, user_logout_view

app_name = "crm"


urlpatterns = [
    path("", main, name="main"),
    path("login/", CrmLoginView.as_view(), name="login_page"),
    path("logout/", user_logout_view, name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("test/", test, name="test")
]

ajax_urlpatterns = [
    path("ajax/login", CrmLoginView.as_view(), name="ajax_login")
]

urlpatterns += ajax_urlpatterns