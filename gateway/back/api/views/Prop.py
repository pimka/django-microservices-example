from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Request, Response

from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests


class PropertyBaseOperView(APIView):
    base = Requests()
    pagination = LimitOffsetPagination()
    pagination.default_limit = 100

    def post(self, request):
        response = self.base.post(self.base.URLS['prop'], request.data)
        json, status = self.base.logging('ADD PROPERTY', response)
        return Response(json, status)

    def get(self, request, limit_offset=None):
        limit_offset = request.query_params
        url = self.base.URLS['prop']
        if limit_offset:
            url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'
        response = self.base.get(url)
        json, status = self.base.logging('GET PROPERTIES', response)

        context = dict()
        if status == 200:
            context['properties'] = json
        return Response(json, status)

class PropertyAdvOperView(APIView):
    base = Requests()
    permission_classes = [IsCustomAuthenticated, ]

    def get(self, request, prop_id):
        response = self.base.get(self.base.URLS['prop'] + f'{prop_id}/')
        json, status = self.base.logging('GET PROPERTY', response)
        return Response(json, status)

    def put(self, request, prop_id):
        response = self.base.put(self.base.URLS['prop'] + f'{prop_id}/', request.data)
        json, status = self.base.logging('UPDATE PROPERTY', response)
        return Response(json, status)

    def delete(self, request, prop_id):
        response = self.base.delete(self.base.URLS['prop'] + f'{prop_id}/')
        json, status = self.base.logging('DELETE PROPERTY', response)
        return Response(json, status)
