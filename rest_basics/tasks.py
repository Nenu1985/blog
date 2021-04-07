import time

from celery import shared_task

from dj_project.celery import app


@app.task
def sleep(seconds: int):
    time.sleep(seconds)
    print('slept')
    return 'Ok'