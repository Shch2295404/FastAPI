from celery import Celery

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks"]
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True
)