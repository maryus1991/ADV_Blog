from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    for return if user create this post or not for edit
    """
    def has_object_permission(self, request, view, obj):
        return object.author.user == request.user