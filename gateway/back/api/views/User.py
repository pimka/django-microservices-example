import pybreaker
from django.core.cache import cache
from requests.exceptions import RequestException
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView, Request, Response

import celery_queue.tasks as tasks
from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests
from api.service_auth import TokeniseRequest
from gateway.settings import ACCESS_DATA

cache.set('user_state', pybreaker.CircuitMemoryStorage(pybreaker.STATE_CLOSED), None)
breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=60, state_storage=cache.get('user_state'))
USER_ID = ACCESS_DATA['user']['app_id']
USER_SECRET = ACCESS_DATA['user']['app_secret']

class UserAuthView(APIView):
    base = Requests()
    pagination = LimitOffsetPagination()
    pagination.default_limit = 100
    
    def post(self, request):

        @TokeniseRequest(cache, USER_ID, USER_SECRET, 'USER', 'http://localhost:8001/serviceAuth/')
        def func(*args, **kwargs):
            return self.base.post(*args, **kwargs)

        try:
            response = breaker.call(func, self.base.URLS['auth'], request.data)
            json, status = self.base.logging('AUTH', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('user_state', breaker._state_storage, None)
            return Response(json, status)

class UserBaseOperView(APIView):
    base = Requests()

    def post(self, request):

        @TokeniseRequest(cache, USER_ID, USER_SECRET, 'USER', 'http://localhost:8001/serviceAuth/')
        def func(*args, **kwargs):
            return self.base.post(*args, **kwargs)

        try:
            response = breaker.call(func, self.base.URLS['user'], request.data)
            json, status = self.base.logging('REGISTRATION', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            tasks.post.delay(self.base.URLS['user'], request.data)
            json = {'error' : 'Service unavailable'}
            status = 503
        return Response(json, status)

    def get(self, request, limit_offset=None):

        @TokeniseRequest(cache, USER_ID, USER_SECRET, 'USER', 'http://localhost:8001/serviceAuth/')
        def func(*args, **kwargs):
            return self.base.get(*args, **kwargs)

        limit_offset = request.query_params
        url = self.base.URLS['user']
        if limit_offset:
            url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'

        try:
            response = breaker.call(func, url, self.base.auth_header(request=request))
            json, status = self.base.logging('GET USERS', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('user_state', breaker._state_storage, None)
            return Response(json, status)

class UserAdvOperView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def get(self, request, user_id):

        @TokeniseRequest(cache, USER_ID, USER_SECRET, 'USER', 'http://localhost:8001/serviceAuth/')
        def func(*args, **kwargs):
            return self.base.get(*args, **kwargs)

        try:
            response = breaker.call(func, self.base.URLS['user'] + f'{user_id}/', self.base.auth_header(request))
            json, status = self.base.logging('GET USER', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('user_state', breaker._state_storage, None)
            return Response(json, status)
