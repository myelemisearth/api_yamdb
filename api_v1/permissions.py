from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            bj.author == request.user
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            request.user.role == 'admin'
        )


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            request.user.role == 'moderator'
        )


class IsUser(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            request.user.role == 'user'
        )

class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser