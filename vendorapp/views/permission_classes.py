from rest_framework import permissions


class ProfilePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT']:
            return True
        return request.user.is_authenticated()


# Api only accessable by seller
class ProductOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if request.user.user_type.lower() in ['seller']:
                return True
        return False


# Api only accessable by customer
class CustomerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if request.user.user_type.lower() in ['customer']:
                return True
        return False
