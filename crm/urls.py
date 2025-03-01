from django.urls import path
from crm.views import (CrmLoginView, DashboardView, test,
                       user_logout_view, ServiceRequestsListView,
                       ServiceRequestCreateView)

app_name = "crm"


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", CrmLoginView.as_view(), name="login_page"),
    path("logout/", user_logout_view, name="logout"),
    path("my-service-requests/", ServiceRequestsListView.as_view(), name="service_requests_list"),
    path("add-service-request/", ServiceRequestCreateView.as_view(), name="add_service_request"),
    path("test", test, name="test/")
]

ajax_urlpatterns = [
    path("ajax/login", CrmLoginView.as_view(), name="ajax_login")
]

urlpatterns += ajax_urlpatterns