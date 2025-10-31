# cheques/urls.py
from django.urls import path
from .views import (
    ChequeUploadView, ChequeDetailView, ChequeVerifyView,
    ChequeListView, VerificationListView, VerificationDetailView,
    ChequeReverifyView,ChequeAuditListView
)

urlpatterns = [
    path("", ChequeUploadView.as_view(), name="cheque-upload"),
    path("list/", ChequeListView.as_view(), name="cheque-list"),
    path("<int:pk>/", ChequeDetailView.as_view(), name="cheque-detail"),
    path("<int:pk>/verify/", ChequeVerifyView.as_view(), name="cheque-verify"),
    path("<int:pk>/reverify/", ChequeReverifyView.as_view(), name="cheque-reverify"),
    path("verifications/", VerificationListView.as_view(), name="verification-list"),
    path("verifications/<int:pk>/", VerificationDetailView.as_view(), name="verification-detail"),

    path("<int:pk>/audit/", ChequeAuditListView.as_view(), name="cheque-audit"),
]
