from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadChequeView.as_view(), name='upload-cheque'),
    path('verify_signatures/', views.VerifySignaturesView.as_view(), name='verify_signatures'),
]
