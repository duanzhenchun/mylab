from celery.schedules import crontab


#http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#available-fields
CELERYBEAT_SCHEDULE = {
    'clean_db': {
        'task': 'tasks.clean_db',
        'schedule': crontab( minute='*/1'),
        'kwargs': {'table':'mytable', 'status':True},
    },
}

CELERY_TIMEZONE = 'Asia/Shanghai'


"""
celery -A tasks beat -l debug --config=beat_conf --pidfile=beat.pid --logfile=beat.log

#monitor
celery -A tasks flower --port=5555
use browser to localhost:5555 
"""
