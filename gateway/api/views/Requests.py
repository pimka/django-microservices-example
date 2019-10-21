import logging

import requests
from rest_framework.views import Request


class Requests:
    URLS = {
        'user':'http://localhost:8001/user/',
        'auth':'http://localhost:8001/auth/',
        'is_exist':'http://localhost:8001/is_exist/',
        'order':'http://localhost:8002/orders/',
        'prop':'http://localhost:8003/props/'
    }
    TOKENS = dict()
    log = logging.getLogger(name='MicroserversLogger')

    def get(self, url, header=None):
        self.log.info(f'GET | {url} | {header}')
        try:
            response = requests.get(url, headers=header)
            return response
        except requests.exceptions.RequestException as err:
            self.log.exception(f'GET | {url} | {header} | {str(err)}')
            return None

    def post(self, url, data, header=None):
        self.log.info(f'POST | {url} | {header} | {data}')
        try:
            response = requests.post(url, json=data, headers=header)
            return response
        except requests.exceptions.RequestException as err:
            self.log.exception(f'POST | {url} | {header} | {str(err)}')
            return None

    def delete(self, url, header=None):
        self.log.info(f'DELETE | {url} | {header}')
        try:
            response = requests.delete(url, headers=header)
            return response
        except requests.exceptions.RequestException as err:
            self.log.exception(f'DELETE | {url} | {header} | {str(err)}')
            return None

    def put(self, url, data, header=None):
        self.log.info(f'PUT | {url} | {header} | {data}')
        try:
            response = requests.put(url, json=data, headers=header)
            return response
        except requests.exceptions.RequestException as err:
            self.log.exception(f'PUT | {url} | {header} | {str(err)}')
            return None

    def get_token(self, request):
        token = request.META['HTTP_AUTHORIZATION']
        return token[7:]

    def auth_header(self, request):
        try:
            return {'Authorization':f'Token {self.get_token(request)}'}
        except KeyError as err:
            return None

    def logging(self, message_type, response):
        self.log.info(f'{message_type} | {response.status_code}')
        try:
            return response.json(), response.status_code
        except ValueError as err:
            self.log.exception(f'{message_type} | {err.msg}')
            return response.text, response.status_code

class UserExist(Requests):
    def is_exist(self, request):
        response = self.get(self.URLS['is_exist'], self.auth_header(request))
        return self.logging('USER EXIST', response)