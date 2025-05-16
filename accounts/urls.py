from django.urls import path
from .views import UserRegistrationView, ObtainTokenView, LogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', ObtainTokenView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
