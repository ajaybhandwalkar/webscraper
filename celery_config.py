from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
import os

load_dotenv()

app = Celery('celery_tasks', broker=os.getenv("CELERY_BROKER_URL"), backend=os.getenv("CELERY_RESULT_BACKEND"))

app.conf.update(
    beat_schedule={
        'run-task-at-midnight': {
            'task': 'scheduler',
            'schedule': crontab(minute="0", hour="0"),  # midnight 00.00AM
        },

        'run-task-every-5-minutes': {
            'task': 'executor',
            'schedule': 60.0,  # every 5 minutes
        }
    },
    result_expires=3600,
)

app.conf.timezone = 'UTC'

