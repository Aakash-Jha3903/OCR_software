# core/urls.py 
from django.urls import path
from .views import AccountCreateView, AccountDetailView, AccountBalancePatchView

urlpatterns = [
    path("", AccountCreateView.as_view(), name="account-create"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account-detail"),
    path("<int:pk>/balance/", AccountBalancePatchView.as_view(), name="account-balance"),
]
