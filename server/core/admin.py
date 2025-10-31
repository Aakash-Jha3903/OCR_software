# core/admin.py
from django.contrib import admin
from .models import Bank, Account

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ifsc_prefix", "micr_prefix", "city")
    search_fields = ("name", "ifsc_prefix", "micr_prefix")

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "holder_name", "account_number", "bank", "balance", "is_active")
    search_fields = ("holder_name", "account_number")
    list_filter = ("bank", "is_active")
