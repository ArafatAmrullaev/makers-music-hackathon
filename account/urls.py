from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, activate, password_confirm

from .views import ChangePasswordView, ResetPasswordView


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<str:activation_code>/', activate),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('api/reset-password/<str:activation_code>/', ResetPasswordView.as_view())
]