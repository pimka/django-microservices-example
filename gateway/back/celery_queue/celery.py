from celery import Celery

celery_app = Celery('celery_queue', broker='redis://localhost:6379/0', include=['celery_queue.tasks'])

if __name__ == "__main__":
    celery_app.start()