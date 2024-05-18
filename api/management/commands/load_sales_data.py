

from django.core.management.base import BaseCommand
from api.utils import load_sales_data
  
  
class Command(BaseCommand): 
    help = 'Loads Sales Data through option -f for filename'
  
    def add_arguments(self, parser): 
        parser.add_argument('-f', '--filename', type=str, help='file path') 
  
    def handle(self, *args, **kwargs): 
        filename = kwargs['filename']
        # error handling
        if not filename:
            print('Please Add Filename')
        else:
            # calling the util method to load data
            load_sales_data(filename)
        
