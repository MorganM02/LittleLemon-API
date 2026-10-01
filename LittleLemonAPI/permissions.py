from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='Manager').exists()
        )


class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='Delivery Crew').exists()
        )


class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='Manager').exists()
        )