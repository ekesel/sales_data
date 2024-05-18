from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import salesData, Tenant
from .serializers import SaleTrendSerializer,StarCustomerSerializer
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Max, Avg
from datetime import datetime

@api_view(['GET'])
def get_max_average_sales(request):
    if request.method == "GET":
        # truncing to month
        sales_with_month = Tenant.objects.annotate(month=TruncMonth('saledate'))
        # getting the average 
        avg_sales_with_month = sales_with_month.values('month').annotate(avg_sales=Avg('sale_amount')).order_by('-avg_sales')
        # taking the top three
        top_three = avg_sales_with_month[:3]
        return Response(top_three, status=200)
    return Response({'error': 'Method invalid'}, status=404)

@api_view(['POST'])
def sale_trends(request):
    # making sure to go in post method only
    if request.method == "POST":
        # serializing the data
        serializer = SaleTrendSerializer(data=request.data)
        # validating
        if serializer.is_valid():
            data = serializer.data
            # filtering the table with payload product id 
            queryset = salesData.objects.filter(product_id=data['product_id'])
            result = {}
            for object in queryset:
                # checking the object belong in that year
                if object.year < data['start_year'] or object.year > data['end_year']:
                    continue
                # chcking the object belong in that month
                if object.month < data['start_month'] or object.month > data['end_month']:
                    continue
                # storing the month wise total sale
                if object.month in result:
                    result[object.month] = result[object.month] + object.total_sale
                else:
                    result[object.month] = object.total_sale
            return Response(result, status=200)
        else:
            # we should log the errors ourselves and send a normal text here to the end user. for now, doing it like this
            return Response({'error': serializer.errors }, status=500)
    return Response({'error': 'Method invalid'}, status=404)

@api_view(['POST'])
def get_star_customer(request):
    # making sure to go in post method only
    if request.method == "POST":
        serializer = StarCustomerSerializer(data=request.data)
        # validating
        if serializer.is_valid():
            result = {}
            data = serializer.data
            start_year = int(data['start_year'])
            end_year = int(data['end_year'])
            # making a year list to query 
            year_list = [year for year in range(start_year, end_year + 1)]
            queryset = Tenant.objects.filter(saledate__year__in=year_list)
            # truncing to month
            sales_with_month = queryset.annotate(month=TruncMonth('saledate'))
            #grouping with total sales amount
            grouped_sales = sales_with_month.values('customer_id', 'month').annotate(total_sales=Sum('sale_amount'))
            # preparing the response with max value
            for sale in grouped_sales:
                dt = sale['month']
                if dt.month in result:
                    if sale['total_sales'] > result[dt.month]['total_sales']:
                        result[dt.month] = {
                            'customer_id': sale['customer_id'],
                            'total_sales': sale['total_sales']
                        }
                else:
                    result[dt.month] = {
                            'customer_id': sale['customer_id'],
                            'total_sales': sale['total_sales']
                        }
            return Response(result, status=200)
        else:
            # we should log the errors ourselves and send a normal text here to the end user. for now, doing it like this
            return Response({'error': serializer.errors }, status=500)
    return Response({'error': 'Method invalid'}, status=404)