from django.urls import path
from crm.views import (CrmLoginView, DashboardView, test,
                       user_logout_view, ServiceRequestsListView,
                       ServiceRequestCreateView, ServiceRequestDetailView)

from crm.ajax_views import (AddNewServiceAjaxView, AddNewClientAjaxView,
                            AddNewServiceRequestAjaxView, AddNewNoteAjaxView,
                            AddAddressForServiceRequest, AjaxChangeTotalPriceForServiceRequest,
                            GetHtmlForCalculateCostPrice, UpdateListOfCostPriceCases,
                            AddCostPriceCaseView, ChangeCurrentCostCaseView,
                            DeleteCostCaseView, CostPriceCaseDetailView)

app_name = "crm"


urlpatterns = [
    path("",
         DashboardView.as_view(),
         name="dashboard"),
    path("login/",
         CrmLoginView.as_view(),
         name="login_page"),
    path("logout/",
         user_logout_view,
         name="logout"),
    path("my-service-requests/",
         ServiceRequestsListView.as_view(),
         name="service_requests_list"),
    path("add-service-request/",
         ServiceRequestCreateView.as_view(),
         name="add_service_request"),
    path("service-request-detail/<int:service_request_id>/",
         ServiceRequestDetailView.as_view(),
         name="service_request_detail"),
    path("test", test,
         name="test/")
]

ajax_urlpatterns = [
    path("ajax/login",
         CrmLoginView.as_view(),
         name="ajax_login"),
    path("ajax/add-new-service",
         AddNewServiceAjaxView.as_view(),
         name="ajax_add_new_service"),
    path("ajax/add-new-client",
         AddNewClientAjaxView.as_view(),
         name="ajax_add_new_client"),
    path("ajax/add-new-service-request",
         AddNewServiceRequestAjaxView.as_view(),
         name="ajax_add_new_request"),
    path("ajax/add-new-note",
         AddNewNoteAjaxView.as_view(),
         name="ajax_add_new_note"),
    path("ajax/add-new-address",
         AddAddressForServiceRequest.as_view(),
         name="ajax_add_new_address"),
    path("ajax/change-request-total-price",
         AjaxChangeTotalPriceForServiceRequest.as_view(),
         name="ajax_change_request_total_price"),
    path("ajax/calculate-cost-price",
         GetHtmlForCalculateCostPrice.as_view(),
         name="ajax_calculate-cost-price"),
    path("ajax/update-calculate-cost-price",
         UpdateListOfCostPriceCases.as_view(),
         name="ajax-update-list-cost-prices"),
    path("ajax/add-cost-price-case",
         AddCostPriceCaseView.as_view(),
         name="ajax_add_cost_price_case"),
    path("ajax/change-current-cost-price-case",
         ChangeCurrentCostCaseView.as_view(),
         name="ajax_change_current_cost_price_case"),
    path("ajax/delete-cost-price-case",
         DeleteCostCaseView.as_view(),
         name="ajax_delete_cost_price_case"),
    path("ajax/cost-price-case-detail",
         CostPriceCaseDetailView.as_view(),
         name="ajax_cost-price-case-detail"),
]

urlpatterns += ajax_urlpatterns