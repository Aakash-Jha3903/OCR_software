# cheques/models.py
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import Account
from .choices import ChequeStatus, Decision

class Cheque(models.Model):
    image = models.ImageField(upload_to="cheques/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, choices=ChequeStatus.choices, default=ChequeStatus.UPLOADED)

    # OCR’d fields
    date_text = models.CharField(max_length=32, blank=True)
    payee = models.CharField(max_length=160, blank=True)
    amount_digits = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    amount_words = models.TextField(blank=True)
    micr = models.CharField(max_length=18, blank=True)
    ocr_raw = models.JSONField(default=dict, blank=True)

    # Linking to detected account (if any)
    detected_account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name="cheques")

    def __str__(self):
        return f"Cheque #{self.pk} ({self.status})"

class Verification(models.Model):
    cheque = models.OneToOneField(Cheque, on_delete=models.CASCADE, related_name="verification")
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    # step outcomes
    is_account_found = models.BooleanField(default=False)
    are_core_fields_matched = models.BooleanField(default=False)
    sign_similarity = models.FloatField(null=True, blank=True)  # 0–100
    sign_threshold = models.FloatField(default=80.0)
    decision = models.CharField(max_length=8, choices=Decision.choices, default=Decision.MANUAL)
    message = models.TextField(blank=True)

    # debit info (final step)
    debit_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True,
                                       validators=[MinValueValidator(Decimal("0"))])
    debit_post_balance = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Verification #{self.pk} for Cheque #{self.cheque_id}"

class ChequeAudit(models.Model):
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name="audits")
    old_status = models.CharField(max_length=32, blank=True)
    new_status = models.CharField(max_length=32)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit #{self.id} for Cheque {self.cheque_id}: {self.old_status} → {self.new_status}"
