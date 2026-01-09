from rest_framework.permissions import BasePermission
from main.models import DONE

class IsAuthenticatedAndAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthenticatedAndDone(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.status==DONE
