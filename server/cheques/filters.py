# cheques/filters.py
import django_filters as df
from .models import Cheque, Verification
from .choices import ChequeStatus, Decision

class ChequeFilter(df.FilterSet):
    status = df.CharFilter(field_name="status", method="status_filter")
    min_amount = df.NumberFilter(field_name="amount_digits", lookup_expr="gte")
    max_amount = df.NumberFilter(field_name="amount_digits", lookup_expr="lte")

    def status_filter(self, qs, name, value):
        try:
            ChequeStatus[value]  # validate
            return qs.filter(status=value)
        except Exception:
            return qs.none()

    class Meta:
        model = Cheque
        fields = ["status", "micr", "payee"]

class VerificationFilter(df.FilterSet):
    decision = df.CharFilter(method="decision_filter")

    def decision_filter(self, qs, name, value):
        try:
            Decision[value]
            return qs.filter(decision=value)
        except Exception:
            return qs.none()

    class Meta:
        model = Verification
        fields = ["decision", "cheque__detected_account__account_number"]
