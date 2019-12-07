import pybreaker
from django.core.cache import cache
from requests.exceptions import RequestException
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Request, Response

from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests
import celery_queue.tasks as tasks

cache.set('prop_state', pybreaker.CircuitMemoryStorage(pybreaker.STATE_CLOSED), None)
breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=60, state_storage=cache.get('prop_state'))


class PropertyBaseOperView(APIView):
    base = Requests()
    pagination = LimitOffsetPagination()
    pagination.default_limit = 100

    def post(self, request):
        try:
            response = breaker.call(self.base.post, self.base.URLS['prop'], request.data)
            json, status = self.base.logging('ADD PROPERTY', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            tasks.post.delay(self.base.URLS['prop'], request.data)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('prop_state', breaker._state_storage, None)
            return Response(json, status)

    def get(self, request, limit_offset=None):
        limit_offset = request.query_params
        url = self.base.URLS['prop']
        if limit_offset:
            url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'
        
        try:
            response = breaker.call(self.base.get, url)
            json, status = self.base.logging('GET PROPERTIES', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('prop_state', breaker._state_storage, None)
            return Response(json, status)

class PropertyAdvOperView(APIView):
    base = Requests()
    permission_classes = [IsCustomAuthenticated, ]

    def get(self, request, prop_id):
        try:
            response = breaker.call(self.base.get, self.base.URLS['prop'] + f'{prop_id}/')
            json, status = self.base.logging('GET PROPERTY', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('prop_state', breaker._state_storage, None)
            return Response(json, status)

    def put(self, request, prop_id):
        try:
            response = breaker.call(self.base.put, self.base.URLS['prop'] + f'{prop_id}/', request.data)
            json, status = self.base.logging('UPDATE PROPERTY', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            tasks.put.delay(self.base.URLS['prop'] + f'{prop_id}/', request.data)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('prop_state', breaker._state_storage, None)
            return Response(json, status)

    def delete(self, request, prop_id):
        try:
            response = breaker.call(self.base.delete, self.base.URLS['prop'] + f'{prop_id}/')
            json, status = self.base.logging('DELETE PROPERTY', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            tasks.delete.delay(self.base.URLS['prop'] + f'{prop_id}/')
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('prop_state', breaker._state_storage, None)
            return Response(json, status)
