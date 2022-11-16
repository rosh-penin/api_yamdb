from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser)

#  Мб убрать? В целом дальше has_permission если юзер не прошел,
    #  то он не дойдет до has_object_permission.
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser)


class IsAdminOrModerOrAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.role == 'moderator' or request.user == obj.author or request.user.is_superuser

