from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'admin' or request.user.is_superuser
                if request.user.is_authenticated else False)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.role == 'admin' or request.user.is_superuser)
                if request.user.is_authenticated else False)


class IsAdminOrModerOrAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user == obj.author or request.user.is_superuser)
