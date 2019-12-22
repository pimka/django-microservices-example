import pybreaker
from django.core.cache import cache
from django.shortcuts import render
from requests.exceptions import RequestException
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Request, Response

import celery_queue.tasks as tasks
from api.permissions import IsCustomAuthenticated
from api.views.Requests import Requests

from .Order import breaker as order_breaker
from .Prop import breaker as prop_breaker
from .User import breaker as user_breaker


class UsersOrdersView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def get(self, request, user_id):
        try:
            limit_offset = request.query_params
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                url = self.base.URLS['order']
                if limit_offset:
                    url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'
                try:
                    response = order_breaker.call(self.base.get, url)
                    json, status = self.base.logging('GET USER ORDERS', response)
                    new_json = []
                    for order in json:
                        if order['customer_uuid'] == str(user_id):
                            new_json.append(order)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    new_json, status = {'error' : 'Service unavailable'}, 503
                    cache.set('order_state', order_breaker._state_storage, None)
            else:
                new_json, status = {'error' : 'User doesn\'t exist'}, 404
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            new_json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(new_json, status)

    def post(self, request, user_id):
        try:
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                try:
                    request.data['customer_uuid'] = str(user_id)
                    response_get_prop = prop_breaker.call(self.base.get, self.base.URLS['prop'] + f'{request.data["prop_uuid"]}/')
                    if response_get_prop.status_code == 200:
                        try:
                            response = order_breaker.call(self.base.post, self.base.URLS['order'], request.data)
                            json, status = self.base.logging('ADD USER ORDER', response)
                        except (RequestException, pybreaker.CircuitBreakerError) as error:
                            self.base.log_exception(error)
                            tasks.post.delay(self.base.URLS['order'], request.data)
                            json, status = {'error' : 'Service unavailable. Enqueued.'}, 503
                            cache.set('order_state', order_breaker._state_storage, None)
                    else:
                        json, status = {'error' : 'Property doesn\'t exist'}, 404
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    json, status = {'error' : 'Service unavailable'}, 503
                    cache.set('prop_state', prop_breaker._state_storage, None)
            else:
                json, status = {'error' : 'User doesn\'t exist'}, 404
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(json, status)


class UserOrdersAdvView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]
    
    def get(self, request, user_id, ord_id):
        try:
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                try:
                    response = order_breaker.call(self.base.get, self.base.URLS['order'] + f'{ord_id}/')
                    json, status = self.base.logging('GET USER ORDER', response)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    json, status = {'error' : 'Service unavailable'}, 503
                    cache.set('order_state', order_breaker._state_storage, None)
            else:
                json, status = {'User doesn\'t exist'}, 404
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(json, status)

    def delete(self, request, user_id, ord_id):
        try:
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                try:
                    response = order_breaker.call(self.base.delete, self.base.URLS['order'] + f'{ord_id}/')
                    json, status = self.base.logging('DELETE USER ORDER', response)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    tasks.delete.delay(self.base.URLS['order'] + f'{ord_id}/')
                    json, status = {'error' : 'Service unavailable. Enqueued'}, 503
                    cache.set('order_state', order_breaker._state_storage, None)
            else:
                json, status = 'User doesn\'t exist', 404
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(json, status)


class UserPropertyView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]
    
    def get(self, request, user_id):
        try:
            limit_offset = request.query_params
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                url = self.base.URLS['prop']
                if limit_offset:
                    url += f'?limit={limit_offset["limit"]}&offset={limit_offset["offset"]}'
                try:
                    response = prop_breaker.call(self.base.get, url)
                    json, status = self.base.logging('GET USER PROPERIES', response)
                    new_json = []
                    for prop in json:
                        if prop['owner_uuid'] == str(user_id):
                            new_json.append(prop)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    cache.set('prop_state', prop_breaker._state_storage, None)
                    new_json, status = {'error' : 'Service unavailable'}, 503
            else:
                new_json, status = {'User doesn\'t exist'}, 404
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            new_json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(new_json, status)

    def post(self, request, user_id):
        try:
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                request.data['owner_uuid'] = str(user_id)
                try:
                    response = prop_breaker.call(self.base.post, self.base.URLS['prop'], request.data)
                    json, status = self.base.logging('ADD USER PROPERTY', response)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    tasks.post.delay(self.base.URLS['prop'], request.data)
                    json, status = {'error' : 'Service unavailable. Enqueued'}, 503
                    cache.set('prop_state', prop_breaker._state_storage, None)
            else:
                return Response('User doesn\'t exist', 404)
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(json, status)
            

class UserPropertyAdvView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def get(self, request, user_id, prop_id):
        try:
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                try:
                    response = prop_breaker.call(self.base.get, self.base.URLS['prop'] + f'{prop_id}/')
                    json, status = self.base.logging('GET USER PROPERTY', response)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    cache.set('prop_state', prop_breaker._state_storage, None)
                    json, status = {'error' : 'Service unavailable'}, 503
            else:
                json, status = {'User doesn\'t exist'}, 404
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(json, status)

    def put(self, request, user_id, prop_id):
        try:
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                try:
                    response = prop_breaker.call(self.base.put, self.base.URLS['prop'] + f'{prop_id}/', response.data)
                    json, status = self.base.logging('PUT USER PROPERTY', response)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    tasks.put.delay(self.base.URLS['prop'] + f'{prop_id}/', response.data)
                    json, status = {'error' : 'Service unavailable. Enqueued'}, 503
            else:
                json, status = {'User doesn\'t exist'}, 404
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(json, status)

    def delete(self, request, user_id, prop_id):
        try:
            response_get_user = user_breaker.call(self.base.get, self.base.URLS['user'] + f'{user_id}/')
            if response_get_user.status_code == 200:
                try:
                    response = prop_breaker.call(self.base.delete, self.base.URLS['prop'] + f'{prop_id}/')
                    json, status = self.base.logging('DELETE USER PROPERTY', response)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    tasks.delete.delay(self.base.URLS['prop'] + f'{prop_id}/')
                    json, status = {'error' : 'Service unavailable. Enqueued'}, 503
            else:
                json, status = {'User doesn\'t exist'}, 404
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            json, status = {'error' : 'Service unavailable'}, 503
        finally:
            cache.set('user_state', user_breaker._state_storage, None)
            return Response(json, status)


class OrderPropView(APIView):
    base = Requests()
    permissions = [IsCustomAuthenticated, ]

    def post(self, request):
        try:
            response_add_order = order_breaker.call(self.base.post, self.base.URLS['order'], request.data['order'])
            json, status = self.base.logging('ADD ORDER WITH PROPERTY', response_add_order)
            if status == 201:
                try:
                    response_add_prop = prop_breaker.call(self.base.post, self.base.URLS['prop'], request.data['prop'])
                    json, status = self.base.logging('ADD ORDER WITH PROPERTY', response_add_prop)
                except (RequestException, pybreaker.CircuitBreakerError) as error:
                    self.base.log_exception(error)
                    order_breaker.call(self.base.delete, self.base.URLS['prop'] + f'{json["order_uuid"]}/')
                    json, status = {'error' : 'Service unavailable'}, 503
        except (RequestException, pybreaker.CircuitBreakerError) as error:
            self.base.log_exception(error)
            tasks.post.delay(self.base.URLS['order'], request.data['order'])
            json, status = {'error' : 'Service unavailable'}, 503
        finally:
            return Response(json, status)
            