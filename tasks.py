from celery import shared_task
import time


@shared_task
def simple_task(_param):
    # Simulate work
    time.sleep(0.0001)
