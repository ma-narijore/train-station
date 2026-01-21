from rest_framework import permissions


class StationPermission(permissions.BasePermission):
    """
    POST, PUT/PATCH, DESTROY allowed only for admin users,
    other methods allowed for authenticated users
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # auth user
            return request.user and request.user.is_authenticated
        # admin
        return request.user and request.user.is_staff
