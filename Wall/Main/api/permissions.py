from rest_framework.permissions import BasePermission

class IsSuperUserOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_superuser or obj.owner == request.user)