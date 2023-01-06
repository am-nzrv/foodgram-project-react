from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Пермишен для админа. Чтение всем."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Пермишен для админа и автора. Чтение всем."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user == obj.author)
                or request.user.is_staff)
