from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            request.user.is_staff

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user != obj.user: 
            return False
        return bool(request.user.is_authenticated and request.user == obj.user)

class IsAuthorOrReadOnly(BasePermission):
    def has_objects_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            request.user.is_authenticated and request.user == obj.user