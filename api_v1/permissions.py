from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            obj.author == request.user
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            request.user.role == 'admin'
        )
    
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsModerator(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            request.user.role == 'moderator'
        )


class ReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
        )
    
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
        )
