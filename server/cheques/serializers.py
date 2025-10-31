# cheques/serializers.py
from rest_framework import serializers
from .models import Cheque, Verification
from core.serializers import AccountReadSerializer

class ChequeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = ["id", "image"]

class ChequeReadSerializer(serializers.ModelSerializer):
    detected_account = AccountReadSerializer(read_only=True)

    class Meta:
        model = Cheque
        fields = [
            "id", "image", "uploaded_at", "status",
            "date_text", "payee", "amount_digits", "amount_words", "micr", "ocr_raw",
            "detected_account"
        ]

class VerificationReadSerializer(serializers.ModelSerializer):
    cheque = ChequeReadSerializer(read_only=True)

    class Meta:
        model = Verification
        fields = [
            "id", "cheque", "started_at", "finished_at",
            "is_account_found", "are_core_fields_matched",
            "sign_similarity", "sign_threshold", "decision", "message",
            "debit_amount", "debit_post_balance"
        ]


from .models import ChequeAudit
class ChequeAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeAudit
        fields = ["id", "old_status", "new_status", "message", "created_at"]
