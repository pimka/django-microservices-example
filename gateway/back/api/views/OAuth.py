from django.core.cache import cache
from requests.exceptions import RequestException
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView, Request, Response

from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests


class TokenExchangeView(APIView):
    base = Requests()

    def post(self, request):
        code = request.data['code']
        data = {
            'grant_type' : 'authorization_code',
            'client_id' : 'in7xsewpL5Hisi0ESPGyGz58HQ1eWhc97zObNMVG',
            'client_secret' : 'SC12l7LpgO3Vu6oIMRSwBjt0ud2y8jCY3Ux1EJ7Vsuul8siu5pIdn9L5P6IeXhv1nRkKQ6WqvG02pLl3EMBIt0EeulDjdOZJnDp5UYzCE9ZGZK7wqTLX9xMQpWdLDTtt',
            'code' : code
        }
        get_token_request = self.base.post(self.base.URLS['oauth'] + 'token/', data)
        json, status = self.base.logging('GET TOKEN', get_token_request)
        return Response(data = json, status = status)