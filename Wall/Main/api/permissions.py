from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Admins have full access.
    """
    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user and request.user.is_staff:
            return True
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the bookmark.
        return obj.user == request.user
    
class IsSuperUserOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_superuser or obj.owner == request.user)