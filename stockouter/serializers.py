from rest_framework import serializers
from .models import *


class StockSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    ticket = serializers.CharField()

    class Meta:
        model = Stock
        fields = "__all__"


class FinancialSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Financial
        fields = "__all__"
