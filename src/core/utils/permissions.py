from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class IsStaffOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            if request.method in SAFE_METHODS:
                return True
            return (request.user.is_authenticated and request.user.is_staff)
        return False


class IsOwnerOrAdmin(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.is_staff


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if super().has_permission(request, view):
            if request.method in SAFE_METHODS:
                return True
            return obj.user == request.user or request.is_staff
        return False
