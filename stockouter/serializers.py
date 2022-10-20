from rest_framework import serializers
from .models import *

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class FinancialSerializer(serializers.ModelSerializer):
    stock=StockSerializer(read_only=True)
    class Meta:
        model = Financial
        fields = '__all__'

class SomeSerializer(serializers.ModelSerializer):
    field1=serializers.CharField(allow_blank=True,default=None)
    field2=serializers.CharField(allow_blank=True,default=None)
    class Meta:
        model = SomeModel
        fields = ['field1','field2']
