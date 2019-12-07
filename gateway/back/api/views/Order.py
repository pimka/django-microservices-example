import pybreaker
from django.core.cache import cache
from requests.exceptions import RequestException
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView, Request, Response

from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests
import celery_queue.tasks as tasks

cache.set('order_state', pybreaker.CircuitMemoryStorage(pybreaker.STATE_CLOSED), None)
breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=60, state_storage=cache.get('order_state'))


class OrderBaseOperView(APIView):
    base = Requests()
    pagination = LimitOffsetPagination()
    pagination.default_limit = 100

    def post(self, request):
        try:
            response = breaker.call(self.base.post, self.base.URLS['order'], request.data)
            json, status = self.base.logging('ADD ORDER', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            tasks.post.delay(self.base.URLS['order'], request.data)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('order_state', breaker._state_storage, None)
            return Response(json, status)

    def get(self, request, limit_offset=None):
        limit_offset = request.query_params
        url = self.base.URLS['order']
        if limit_offset:
            url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'

        try:
            response = breaker.call(self.base.get, url)
            json, status = self.base.logging('GET ORDERS', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('order_state', breaker._state_storage, None)
            return Response(json, status)

class OrderAdvOperView(APIView):
    base = Requests()
    permission_classes = [IsCustomAuthenticated, ]

    def get(self, request, ord_id):
        try:
            response = breaker.call(self.base.get, self.base.URLS['order'] + f'{ord_id}/')
            json, status = self.base.logging('GET ORDER', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('order_state', breaker._state_storage, None)
            return Response(json, status)

    def put(self, request, ord_id):
        try:
            response = breaker.call(self.base.put, self.base.URLS['order'] + f'{ord_id}/', request.data)
            json, status = self.base.logging('UPDATE ORDER', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            tasks.put.delay(self.base.URLS['order'] + f'{ord_id}/', request.data)
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('order_state', breaker._state_storage, None)
            return Response(json, status)

    def delete(self, request, ord_id):
        try:
            response = breaker.call(self.base.delete, self.base.URLS['order'] + f'{ord_id}/')
            json, status = self.base.logging('DELETE ORDER', response)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            tasks.delete.delay(self.base.URLS['order'] + f'{ord_id}/')
            json = {'error' : 'Service unavailable'}
            status = 503
        finally:
            cache.set('order_state', breaker._state_storage, None)
            return Response(json, status)
