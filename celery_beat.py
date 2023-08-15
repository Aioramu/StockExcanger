import os

from celery import Celery, signature
from celery.schedules import crontab
from django.conf import settings

from stockex import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockex.settings')

celery_app = Celery('site', backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.conf.imports = ["stockrouter.tasks"]


celery_app.conf.beat_schedule = {
    'update_macrotrends': {
        'task': 'stockrouter.tasks.get_macrotrends_values',
        'schedule': crontab(minute='48', hour='14'),
    },

}
