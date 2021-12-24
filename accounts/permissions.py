# third party imports
from rest_framework import permissions


# local imports


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Allows access only to Superuser users.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

        return request.method in permissions.SAFE_METHODS
