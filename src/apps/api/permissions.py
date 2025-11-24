"""API permissions."""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read-only for all, write for admin only."""

    def has_permission(self, request, view):
        """Check permission."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
