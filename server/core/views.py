# core/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation
from .models import Account
from .serializers import AccountCreateSerializer, AccountReadSerializer

class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer
    permission_classes = [permissions.AllowAny]

class AccountDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountReadSerializer
    permission_classes = [permissions.AllowAny]

class AccountBalancePatchView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountReadSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, *args, **kwargs):
        account = self.get_object()
        try:
            amount = Decimal(str(request.data.get("amount", "0")))
        except InvalidOperation:
            return Response({"detail": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        op = request.data.get("op", "debit").lower()
        if op not in {"debit", "credit"}:
            return Response({"detail": "op must be 'debit' or 'credit'."}, status=status.HTTP_400_BAD_REQUEST)

        if op == "debit":
            if amount > account.balance:
                return Response({"detail": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)
            account.balance -= amount
        else:
            account.balance += amount

        account.save()
        return Response(AccountReadSerializer(account).data)
