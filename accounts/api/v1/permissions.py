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