from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Allow any access to admin role or superuser."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin'
                                                  or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    """Allow any access to admin role or superuser. Others can read only."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and request.user.role
                    == 'admin' or request.user.is_superuser))


class IsAdminOrModerOrAuthorOrReadOnly(BasePermission):
    """All users and anonymous can read only.
    Authenticated users have access to the list actions.
    Only author of object, moderator or admin or superuser
    can manipulate an object.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user == obj.author or request.user.is_superuser)
