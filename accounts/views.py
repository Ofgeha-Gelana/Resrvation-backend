from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer, TokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.views import APIView
from rest_framework import status

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

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            print(refresh_token)
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)
