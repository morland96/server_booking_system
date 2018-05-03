from datetime import timedelta
from datetime import datetime
from celery import Celery

app = Celery(
    'tasks', broker='amqp://admin:admin@localhost/myvhost', backend='amqp://')
app.conf.timezone = 'Asia/Shanghai'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(crontab(, add.s(2, 2), name='add every 2s')
    add.apply_async(expires=datetime.datetime.utcnow() + timedelta(seconds=2))
    print("....")


@app.create_user
def create_user():
    pass


@app.task
def add(x, y):
    print(x + y)
    return x + y
