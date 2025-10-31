# cheques/admin.py
from django.contrib import admin
from .models import Cheque, Verification

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ("id", "uploaded_at", "status", "payee", "amount_digits", "micr", "detected_account")
    search_fields = ("micr", "payee")
    list_filter = ("status",)

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "cheque", "decision", "sign_similarity", "debit_amount")
    list_filter = ("decision",)
