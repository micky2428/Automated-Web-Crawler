
# from celery import Celery

# app = Celery(
#     "task",
#     # include=["shopData.tasks.task"],
#     include=["tasks"],
#     broker="pyamqp://worker:worker@localhost:5672/",
# )

from celery import Celery
from shopData.config import (
    WORKER_ACCOUNT,
    WORKER_PASSWORD,
    MESSAGE_QUEUE_HOST,
    MESSAGE_QUEUE_PORT,
)

broker = (
    f"pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@"
    f"{MESSAGE_QUEUE_HOST}:{MESSAGE_QUEUE_PORT}/"
)
app = Celery(
    "task",
    include=["shopData.tasks.task"],
    broker=broker,
)
