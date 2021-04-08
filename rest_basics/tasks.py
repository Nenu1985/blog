import time

from dj_project.celery import app


@app.task
def sleep(seconds: int):
    time.sleep(seconds)
    print('slept')
    return 'Ok'
