from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated  


from .serializers import RegisterSerializer, ResetPasswordSerializer

User = get_user_model()

from drf_yasg.utils import swagger_auto_schema
class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Вы успешно зарегистрировались!")

@api_view(["GET"])
def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    return redirect("http://127.0.0.1:3000/")

# @api_view(["GET"])
# def password_confirm(request, new_password):
#     user = get_object_or_404(User, new_password=new_password)
#     user.is_active = True
#     user.activation_code = ''
#     user.save()
#     return redirect("https://makerskg-music.herokuapp.com/account/api/reset-password/")

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ResetPasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ResetPasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)