# server/usersapi/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import UserProfile, Account, Bank

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated):
        email = validated["email"].lower()
        password = validated["password"]
        user, created = User.objects.get_or_create(username=email, defaults={"email": email})
        if not created:
            raise serializers.ValidationError("Email already registered.")
        user.set_password(password)
        user.save()
        UserProfile.objects.get_or_create(user=user, defaults={
            "full_name": validated.get("full_name", ""),
            "phone": validated.get("phone", ""),
        })
        return user

    def to_representation(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "id": user.id,
            "email": user.email,
            "token": str(refresh.access_token),
            "refresh": str(refresh),
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].lower()
        pwd = attrs["password"]
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.check_password(pwd):
            raise serializers.ValidationError("Invalid credentials.")
        attrs["user"] = user
        return attrs

    def to_representation(self, attrs):
        user = attrs["user"]
        refresh = RefreshToken.for_user(user)
        return {
            "token": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": getattr(user.profile, "full_name", ""),
                "phone": getattr(user.profile, "phone", ""),
            },
        }

class MeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="profile.full_name", required=False, allow_blank=True)
    phone = serializers.CharField(source="profile.phone", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone"]
        read_only_fields = ["email"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        profile.full_name = profile_data.get("full_name", profile.full_name)
        profile.phone = profile_data.get("phone", profile.phone)
        profile.save()
        return instance

class MeBankSerializer(serializers.Serializer):
    bank = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all(), required=False)
    bank_name = serializers.CharField(required=False, allow_blank=True)
    ifsc = serializers.CharField(required=False, allow_blank=True)
    micr = serializers.CharField(required=False, allow_blank=True)
    account_number = serializers.CharField()
    holder_name = serializers.CharField()
    signature_image = serializers.ImageField(required=False, allow_null=True)
    cancelled_cheque_image = serializers.ImageField(required=False, allow_null=True)

    def create_or_update(self, user):
        data = self.validated_data
        bank = data.get("bank")
        # allow either known bank (id) or free-text bank_name/ifsc/micr (optional)
        if not bank and data.get("bank_name"):
            bank, _ = Bank.objects.get_or_create(
                name=data["bank_name"],
                defaults={
                    "ifsc_prefix": data.get("ifsc", "")[:5],
                    "micr_prefix": data.get("micr", "")[:3],
                    "city": "",
                },
            )
        acc, created = Account.objects.get_or_create(
            owner=user,
            account_number=data["account_number"],
            defaults={
                "bank": bank,
                "holder_name": data["holder_name"],
                "balance": 0,
            },
        )
        # update fields
        if bank:
            acc.bank = bank
        acc.holder_name = data["holder_name"]
        if data.get("signature_image"):
            acc.signature_image = data["signature_image"]
        if data.get("cancelled_cheque_image"):
            acc.cancelled_cheque_image = data["cancelled_cheque_image"]
        acc.save()
        return acc

    def to_representation(self, acc: Account):
        return {
            "id": acc.id,
            "bank": acc.bank.id if acc.bank_id else None,
            "account_number": acc.account_number,
            "holder_name": acc.holder_name,
            "signature_image": acc.signature_image.url if acc.signature_image else None,
            "cancelled_cheque_image": acc.cancelled_cheque_image.url if acc.cancelled_cheque_image else None,
            "balance": str(acc.balance),
            "is_active": acc.is_active,
        }
