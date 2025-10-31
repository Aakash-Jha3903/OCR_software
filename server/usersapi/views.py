from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer, LoginSerializer, MeSerializer, MeBankSerializer
)

class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(ser.to_representation(user), status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]  # <-- ensure
    serializer_class = LoginSerializer
    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]  # <-- ensure
    serializer_class = MeSerializer
    def get_object(self):
        return self.request.user

class MeBankUpsertView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # <-- ensure
    serializer_class = MeBankSerializer
    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        acc = ser.create_or_update(request.user)
        return Response(ser.to_representation(acc), status=status.HTTP_200_OK)
