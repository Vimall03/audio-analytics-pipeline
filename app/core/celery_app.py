from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    'task',
    task_track_started=True,
    backend=os.getenv('CELERY_RESULT_BACKEND'),
    broker=os.getenv('CELERY_BROKER_URL'),
)
celery.conf.broker_connection_retry_on_startup = True