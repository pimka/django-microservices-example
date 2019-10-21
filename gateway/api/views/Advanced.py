from django.shortcuts import render
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Request, Response

from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests


class UsersOrdersView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def get(self, request, user_id):
        limit_offset = request.query_params
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            url = self.base.URLS['order']
            if limit_offset:
                url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'
            response = self.base.get(url)
            json, status = self.base.logging('GET USER ORDERS', response)
            new_json = []
            for order in json:
                if order['customer_uuid'] == str(user_id):
                    new_json.append(order)
            return Response(new_json, status)
        else:
            return Response('User doesn\'t exist', 404)

    def post(self, request, user_id):
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            request.data['customer_uuid'] = str(user_id)
            response_get_prop = self.base.get(self.base.URLS['prop'] + f'{request.data["prop_uuid"]}/')
            if response_get_prop.status_code == 200:
                response = self.base.post(self.base.URLS['order'], request.data)
                json, status = self.base.logging('ADD USER ORDER', response)
                return Response(json, status)
            else:
                return Response('Property doesn\'t exist', 404)
        else:
            return Response('User doesn\'t exist', 404)


class UserOrdersAdvView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def get(self, request, user_id, ord_id):
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            response = self.base.get(self.base.URLS['order'] + f'{ord_id}/')
            json, status = self.base.logging('GET USER ORDER', response)
            return Response(json, status)
        else:
            return Response('User doesn\'t exist', 404)

    def delete(self, request, user_id, ord_id):
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            response = self.base.delete(self.base.URLS['order'] + f'{ord_id}/')
            json, status = self.base.logging('DELETE USER ORDER', response)
            return Response(json, status)
        else:
            return Response('User doesn\'t exist', 404)


class UserPropertyView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def get(self, request, user_id):
        limit_offset = request.query_params
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            url = self.base.URLS['prop']
            if limit_offset:
                url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'
            response = self.base.get(url)
            json, status = self.base.logging('GET USER PROPERIES', response)
            new_json = []
            for prop in json:
                if prop['owner_uuid'] == str(user_id):
                    new_json.append(prop)
            return Response(new_json, status)
        else:
            return Response('User doesn\'t exist', 404)

    def post(self, request, user_id):
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            request.data['owner_uuid'] = str(user_id)
            response = self.base.post(self.base.URLS['prop'], request.data)
            json, status = self.base.logging('ADD USER PROPERTY', response)
            return Response(json, status)
        else:
            return Response('User doesn\'t exist', 404)
            

class UserPropertyAdvView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def get(self, request, user_id, prop_id):
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            response = self.base.get(self.base.URLS['prop'] + f'{prop_id}/')
            json, status = self.base.logging('GET USER PROPERTY', response)
            return Response(json, status)
        else:
            return Response('User doesn\'t exist', 404)

    def put(self, request, user_id, prop_id):
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            response = self.base.put(self.base.URLS['prop'] + f'{prop_id}/', response.data)
            json, status = self.base.logging('PUT USER PROPERTY', response)
            return Response(json, status)
        else:
            return Response('User doesn\'t exist', 404)

    def delete(self, request, user_id, prop_id):
        response_get_user = self.base.get(self.base.URLS['user'] + f'{user_id}/')
        if response_get_user.status_code == 200:
            response = self.base.delete(self.base.URLS['prop'] + f'{prop_id}/')
            json, status = self.base.logging('DELETE USER PROPERTY', response)
            return Response(json, status)
        else:
            return Response('User doesn\'t exist', 404)
