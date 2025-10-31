# core/models.py (Bank + Account)
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Bank(models.Model):
    name = models.CharField(max_length=120)
    ifsc_prefix = models.CharField(max_length=5, blank=True, help_text="e.g., HDFC0, SBIN0")
    micr_prefix = models.CharField(max_length=9, blank=True, help_text="optional MICR routing prefix")
    city = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.name

from django.conf import settings
from django.db import models

# ... existing Bank, Account remain

# 4a) Link Account to the authenticated user (owner) + cancelled cheque image
class Account(models.Model):
    bank = models.ForeignKey("core.Bank", on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=32, db_index=True)
    holder_name = models.CharField(max_length=128)
    signature_image = models.ImageField(upload_to="signatures/")
    # NEW:
    cancelled_cheque_image = models.ImageField(upload_to="cancelled_cheques/", blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="accounts")
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.holder_name} • {self.account_number}"

# 4b) Simple user profile for extra KYC fields (keeps default User; no custom user needed)
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Profile({self.user_id})"
