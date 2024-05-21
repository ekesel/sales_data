

import os 
from celery import Celery 
  
# set the default Django settings module for the 'celery' program. 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salesdata.settings') 
  
app = Celery('salesdata') 

# Using a string here means the worker doesn't  
# have to serialize the configuration object to  
# child processes. - namespace='CELERY' means all  
# celery-related configuration keys should  
# have a `CELERY_` prefix. 
app.config_from_object('django.conf:settings', namespace='CELERY') 
  
# Load task modules from all registered Django app configs. 
app.autodiscover_tasks() 

app.conf.beat_schedule = {
    'load_data_every_day': {
        'task': 'api.tasks.load_sales',
        'schedule': 30.0,
        'args': ('saledata2.csv',),
        'options': {
            'expires': 150.0,
        },
    },
}