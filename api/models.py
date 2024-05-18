from django.db import models

# Create your models here.

class Tenant(models.Model):
    saledate = models.DateTimeField()
    customer_id = models.IntegerField() # these two ids can be foreign keys depending upon more data
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_amount = models.DecimalField(max_digits=6, decimal_places=2)
    data_source = models.CharField(max_length=10, default='csv')

class salesData(models.Model):
    total_sale = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    month = models.IntegerField()
    year = models.CharField(max_length=5)
    product_id = models.IntegerField()