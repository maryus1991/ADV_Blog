from rest_framework import permissions


class NotAuthenticatedPermissions(permissions.BasePermission):
    # create this permission for detect not authed request

    def has_object_permission(self, request, *args, **kwargs):
        # check if user is login or not with request 
        # return true if user is not log in and false if user is log in 
        if not request.user.is_authenticated:
            return True
        else: 
            return False


class IsOwner(permissions.BasePermission):
    # create this permission for detect user is owner or not 

    def has_object_permission(self, request, view, object):
        # user the request and object to check is the user is owner or not to see this info

        # return True if the user is admin
        if request.user.is_superuser:
            return True

        # check if user is log in or not
        if not request.user.is_authenticated:
            return False

        return object.id == request.user.id