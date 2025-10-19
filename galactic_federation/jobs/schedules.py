from __future__ import annotations
from .worker import celery_app

celery_app.conf.beat_schedule = {
    'daily-tick': {
        'task': 'galactic_federation.jobs.worker.daily_tick',
        'schedule': 60.0 * 60.0 * 24.0,
    }
}
