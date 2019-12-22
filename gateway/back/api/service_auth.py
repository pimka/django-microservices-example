from functools import wraps
from api.views.Requests import Requests

class TokeniseRequest():
    def __init__(self, cache, _id, secret, service_name, service_url, _type='Bearer'):
        self.cache = cache
        self._id, self.secret = _id, secret
        self.service_name, self.service_url = service_name, service_url
        self._type = _type
        self.base = Requests()

    def get_token(self):
        response = self.base.post(self.service_url, { 'app_id' : self._id, 'app_secret' : self.secret })
        json, status = self.base.logging(f'GET TOKEN FOR {self.service_name}', response)
        
        if status == 200:
            self.cache.set(self.service_name, json['token'], 3600)

    def make_header(self):
        token = self.cache.get(self.service_name)

        if token is None:
            return {}
        else:
            return {'Authorization': f'{self._type} {token}'}

    def __call__(self, function):
        return self.decorate(function)

    def decorate(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return self.call(function, *args, **kwargs)

        return wrapper

    def call(self, function, *args, **kwargs):
        token = self.cache.get(self.service_name)

        if token is not None:
            kwargs['header'] = self.make_header()
            response = function(*args, **kwargs)

            if response.status_code != 402:
                return response
        
        self.get_token()
        kwargs['header'] = self.make_header()
        response = function(*args, **kwargs)
        return response