from .celery import celery_app
from requests.exceptions import RequestException
from api.views.Requests import Requests

MAIN_REQ = Requests()
# celery -A celery_queue worker -l info -P gevent

@celery_app.task(autoretry_for=(RequestException,), retry_kwargs={ 'max_retries' : 5 }, retry_backoff=True)
def post(url, data, header=None):
    MAIN_REQ.post(url, data, header)

@celery_app.task(autoretry_for=(RequestException,), retry_kwargs={ 'max_retries' : 5 }, retry_backoff=True)
def put(url, data, header=None):
    MAIN_REQ.put(url, data, header)

@celery_app.task(autoretry_for=(RequestException,), retry_kwargs={ 'max_retries' : 5 }, retry_backoff=True)
def delete(url, data, header=None):
    MAIN_REQ.delete(url, header)
