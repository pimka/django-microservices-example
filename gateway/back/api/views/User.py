from django.shortcuts import render
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView, Request, Response

from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests


class UserAuthView(APIView):
    base = Requests()
    pagination = LimitOffsetPagination()
    pagination.default_limit = 100
    
    def post(self, request):
        response = self.base.post(self.base.URLS['auth'], request.data)
        json, status = self.base.logging('AUTH', response)
        return Response(json, status)

class UserBaseOperView(APIView):
    base = Requests()

    def post(self, request):
        response = self.base.post(self.base.URLS['user'], request.data)
        json, status = self.base.logging('REGISTRATION', response)
        return Response(json, status)

    def get(self, request, limit_offset=None):
        limit_offset = request.query_params
        url = self.base.URLS['user']
        if limit_offset:
            url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'
        response = self.base.get(url, self.base.auth_header(request=request))
        json, status = self.base.logging('GET USERS', response)

        context = dict()
        if status == 200:
            context['users'] = json
        return Response(json, status)

class UserAdvOperView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def get(self, request, user_id):
        response = self.base.get(self.base.URLS['user'] + f'{user_id}/', self.base.auth_header(request))
        json, status = self.base.logging('GET USER', response)
        return Response(json, status)
