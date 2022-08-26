from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, activate

from .views import ChangePasswordView
from .views import Home # new

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<str:activation_code>/', activate),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path("accounts/", include("allauth.urls")),
    path("", Home.as_view(), name="home"),
    ]