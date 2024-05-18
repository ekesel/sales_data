from celery import shared_task
from .utils import load_sales_data


# shared task to run from celery beat scheduler, it will just call the util method
@shared_task()
def load_sales(filename):
    load_sales_data(filename)
    return None