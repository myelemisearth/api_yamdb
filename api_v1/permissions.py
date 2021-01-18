from rest_framework.permissions import BasePermission


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
