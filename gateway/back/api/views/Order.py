from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView, Request, Response

from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests


class OrderBaseOperView(APIView):
    base = Requests()
    pagination = LimitOffsetPagination()
    pagination.default_limit = 100

    def post(self, request):
        response = self.base.post(self.base.URLS['order'], request.data)
        json, status = self.base.logging('ADD ORDER', response)
        return Response(json, status)

    def get(self, request, limit_offset=None):
        limit_offset = request.query_params
        url = self.base.URLS['order']
        if limit_offset:
            url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'
        response = self.base.get(url)
        json, status = self.base.logging('GET ORDERS', response)

        context = dict()
        if status == 200:
            context['orders'] = json
        return Response(json, status)

class OrderAdvOperView(APIView):
    base = Requests()
    permission_classes = [IsCustomAuthenticated, ]

    def get(self, request, ord_id):
        response = self.base.get(self.base.URLS['order'] + f'{ord_id}/')
        json, status = self.base.logging('GET ORDER', response)
        return Response(json, status)

    def put(self, request, ord_id):
        response = self.base.put(self.base.URLS['order'] + f'{ord_id}/', request.data)
        json, status = self.base.logging('UPDATE ORDER', response)
        return Response(json, status)

    def delete(self, request, ord_id):
        response = self.base.delete(self.base.URLS['order'] + f'{ord_id}/')
        json, status = self.base.logging('DELETE ORDER', response)
        return Response(json, status)
