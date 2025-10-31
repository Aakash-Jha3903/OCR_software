# core/serializers.py
from rest_framework import serializers
from .models import Bank, Account

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ["id", "name", "ifsc_prefix", "micr_prefix", "city"]

class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "bank", "account_number", "holder_name", "signature_image", "balance", "is_active"]

class AccountReadSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    class Meta:
        model = Account
        fields = ["id", "bank", "account_number", "holder_name", "signature_image", "balance", "is_active"]
