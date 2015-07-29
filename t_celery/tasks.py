import os
import time
from datetime import datetime

from celery import Celery


BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


celery = Celery("tasks", broker="redis://", backend=CELERY_RESULT_BACKEND)
#print celery.conf.get('CELERY_RESULT_BACKEND')


@celery.task
def add(x, y):
    return int(x) + int(y)


@celery.task
def sleep(seconds):
    time.sleep(float(seconds))
    return seconds


@celery.task
def echo(msg, timestamp=False):
    return "%s: %s" % (datetime.now(), msg) if timestamp else msg


@celery.task
def error(msg):
    raise Exception(msg)

@celery.task
def clean_db(table='', status=True):
    if table != '':
        return "delete from %s where status=%s" %(table, status)
    else:
        return 'empty table name'

if __name__ == "__main__":
    celery.start()

"""
celery -A tasks worker -l debug --pidfile=worker.pid --logfile=worker.log&
"""
