# cheques/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, throttling
from rest_framework.response import Response

from .models import Cheque, Verification
from .serializers import ChequeUploadSerializer, ChequeReadSerializer, VerificationReadSerializer
from .pagination import DefaultPagination
from .filters import ChequeFilter, VerificationFilter
from services.verification_service import VerificationService

class BurstThrottle(throttling.AnonRateThrottle):
    rate = "20/min"

class ChequeUploadView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    
    queryset = Cheque.objects.all()
    serializer_class = ChequeUploadSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [BurstThrottle]

class ChequeDetailView(generics.RetrieveAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeReadSerializer
    permission_classes = [permissions.AllowAny]

class ChequeListView(generics.ListAPIView):
    queryset = Cheque.objects.all().order_by("-uploaded_at")
    serializer_class = ChequeReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChequeFilter
    pagination_class = DefaultPagination
    permission_classes = [permissions.AllowAny]

class ChequeVerifyView(generics.GenericAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeReadSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [BurstThrottle]

    def post(self, request, *args, **kwargs):
        cheque = self.get_object()
        threshold = request.data.get("sign_threshold")
        v = VerificationService.verify_cheque(cheque, sign_threshold=threshold)
        return Response(VerificationReadSerializer(v).data, status=status.HTTP_200_OK)

class ChequeReverifyView(ChequeVerifyView):
    """Allows re-run (e.g., after tuning threshold)."""

class VerificationListView(generics.ListAPIView):
    queryset = Verification.objects.select_related("cheque", "cheque__detected_account").order_by("-started_at")
    serializer_class = VerificationReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VerificationFilter
    pagination_class = DefaultPagination
    permission_classes = [permissions.AllowAny]

class VerificationDetailView(generics.RetrieveAPIView):
    queryset = Verification.objects.select_related("cheque", "cheque__detected_account")
    serializer_class = VerificationReadSerializer
    permission_classes = [permissions.AllowAny]


from rest_framework import generics, permissions
from .models import Cheque, ChequeAudit
from .serializers import ChequeAuditSerializer

class ChequeAuditListView(generics.ListAPIView):
    serializer_class = ChequeAuditSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        cheque_id = self.kwargs["pk"]
        return ChequeAudit.objects.filter(cheque_id=cheque_id).order_by("-created_at")
