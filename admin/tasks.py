from engine import Engine
from celery import Celery
from time import sleep
import os
import time

host = os.environ.get('TEST_URL')
login = os.environ.get('RABBITMQ_USER')
password = os.environ.get('RABBITMQ_PASS')

broker_url = f'amqp://{login}:{password}@{host}:5672'
system = Engine()

app = Celery(broker_url, broker=broker_url)


@app.task
def say_hello():
    sleep(15)
    system.start()
    say_hello().delay()


say_hello()
