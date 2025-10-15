from __future__ import annotations
from celery import Celery
from ..core.settings import get_settings

settings = get_settings()
celery_app = Celery('gf', broker=settings.redis_url, backend=settings.redis_url)

@celery_app.task
def daily_tick():
    # TODO: assign issues to planets; send notifications
    return 'ok'
