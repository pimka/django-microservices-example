from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from api.views.Requests import UserExist

class IsCustomAuthenticated(BasePermission):
    def has_permission(self, request, view):
        json, status = UserExist().is_exist(request)
        return status == 200