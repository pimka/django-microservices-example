import logging

import requests


class Requests:
    URLS = {
        'user':'http://localhost:8001/user/',
        'auth':'http://localhost:8001/auth/',
        'is_exist':'http://localhost:8001/is_exist/',
        'order':'http://localhost:8002/orders/',
        'prop':'http://localhost:8003/props/',
        'oauth':'http://localhost:8001/o/',
    }
    TOKENS = dict()
    log = logging.getLogger(name='MicroserversLogger')

    def get(self, url, header=None):
        self.log.info(f'GET | {url} | {header}')
        response = requests.get(url, headers=header)
        return response

    def post(self, url, data, header=None):
        self.log.info(f'POST | {url} | {header} | {data}')
        response = requests.post(url, json=data, headers=header)
        return response

    def delete(self, url, header=None):
        self.log.info(f'DELETE | {url} | {header}')
        response = requests.delete(url, headers=header)
        return response

    def put(self, url, data, header=None):
        self.log.info(f'PUT | {url} | {header} | {data}')
        response = requests.put(url, json=data, headers=header)
        return response

    def get_token(self, request):
        token = request.META['HTTP_AUTHORIZATION']
        return token

    def auth_header(self, request):
        try:
            return {'Authorization':f'Token {self.get_token(request)}'}
        except KeyError as err:
            return None

    def logging(self, message_type, response):
        if response is None:
            self.log.exception(f'Invalid response')
            return ({'error':'Invalid response'}, 503)
        try:
            self.log.info(f'{message_type} | {response.status_code}')
            return response.json(), response.status_code
        except Exception as err:
            self.log.exception(f'{message_type} | {str(err)}')
            return response.text, response.status_code

    def log_exception(self, err):
        self.log.exception(str(err))

class UserExist(Requests):
    def is_exist(self, request):
        response = self.get(self.URLS['is_exist'], self.auth_header(request))
        return self.logging('USER EXIST', response)
