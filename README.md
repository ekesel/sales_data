# sales_data

# made three endpoints
## get_max_average_sales (GET)
## sale_trends (POST)
{
    "start_year": "2023",
    "end_year": "2024",
    "product_id: 4,
    "start_month": 2,
    "end_month: 4
}
## get_star_customer (POST) 
{
    "start_year": "2023",
    "end_year": "2024"
}

## made one management command to load data -> 
python manage.py load_sales_data -f sales_data.csv

### made a celery beat scheduler to load data periodically (currently set to 15 sec, can be changed to run at every 23 hrs)

