from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer, TokenSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # <--- Add this

class ObtainTokenView(generics.GenericAPIView):
    serializer_class = TokenSerializer
    permission_classes = [permissions.AllowAny]  # <--- Add this

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response({"detail": "Invalid credentials"}, status=400)
