from celery import shared_task
from .utils import load_sales_data

@shared_task()
def load_sales(filename):
    load_sales_data(filename)
    return None