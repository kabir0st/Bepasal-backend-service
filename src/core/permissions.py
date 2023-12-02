from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)


class IsAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.is_staff
        return False


class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (True
                if request.method in SAFE_METHODS else request.user.is_staff)
