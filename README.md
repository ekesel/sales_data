# sales_data

# made three endpoints
get_max_average_sales
sale_trends
get_star_customer

# made one management command to load data -> 
python manage.py load_sales_data -f sales_data.csv

# made a celery beat scheduler to load data periodically (currently set to 15 sec, can be changed to run at every 23 hrs)

