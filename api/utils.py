import pandas as pd
from datetime import datetime
from api.models import Tenant, salesData
from decimal import Decimal


#this function will read the csv and perform cleaning
def load_sales_data(filename):
    try:
        df = pd.read_csv(filename)
        # getting the rows index which contains at least a none value
        null_values = df[df.isnull().any(axis=1)].index.to_list()
        # dropping those null values
        df.drop(df.index[null_values], inplace=True)
        count = 0
        for ind, row in df.iterrows():
            try:
                dt = datetime.strptime(row['SaleDate'], '%d/%m/%Y')
                if int(row['SaleAmount']) <= 0:
                    continue
                Tenant.objects.create(saledate=dt,customer_id=row['CustomerId'],product_id=row['ProductId'],
                                      quantity=row['Quantity'],
                                      price=row['Price'],
                                      sale_amount=row['SaleAmount'])
                count += 1
                product_id = int(row['ProductId'])
                queryset = salesData.objects.filter(month=str(dt.month), year=str(dt.year))
                amount = Decimal(row['SaleAmount'])
                if not queryset:
                    salesData.objects.create(month=str(dt.month), year=str(dt.year),
                                             product_id=product_id,total_sale=amount,quantity=row['Quantity'])
                else:
                    if queryset.filter(product_id=product_id).exists():
                        obj = queryset.filter(product_id=product_id).last()
                        obj.total_sale = Decimal(obj.total_sale + amount),
                        obj.quantity = obj.quantity + row['Quantity']
                        obj.save()
                    else:
                        salesData.objects.create(month=str(dt.month), year=str(dt.year),
                                             product_id=product_id,total_sale=amount,quantity=row['Quantity'])
            except Exception as e:
                print(str(e))
        msg = "DATA INGESTION AND CLEANING DONE, TOTAL TENANT ROWS ADDED = %s" % (count)
        print(msg)
        # data transformations
        print(salesData.objects.all())
        
    except Exception as e:
        print("FAILED TO READ FILE")
    