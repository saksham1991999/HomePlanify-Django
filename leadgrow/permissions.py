from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsBusinessOwner(BasePermission):
    """
    Object-level permission to only allow owners of Business to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCustomerBusinessOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.business.user == request.user


class IsTaskBusinessOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.customer.business.user == request.user


class IsNoteBusinessOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.customer.business.user == request.user

