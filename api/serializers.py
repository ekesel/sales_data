from rest_framework import serializers

class SaleTrendSerializer(serializers.Serializer):
    start_year = serializers.CharField()
    end_year = serializers.CharField()
    start_month = serializers.IntegerField()
    end_month = serializers.IntegerField()
    product_id = serializers.IntegerField()

    def validate(self, data):
        """
        Check that start_year is before end_year
        """
        if data['start_year'] > data['end_year']:
            raise serializers.ValidationError("end_year must occur after start_year")
        return data

class StarCustomerSerializer(serializers.Serializer):
    start_year = serializers.CharField()
    end_year = serializers.CharField()

    def validate(self, data):
        """
        Check that start_year is before end_year
        """
        if data['start_year'] > data['end_year']:
            raise serializers.ValidationError("end_year must occur after start_year")
        return data