from django.shortcuts import render
from .models import *
from .serializers import StockSerializer, FinancialSerializer
from rest_framework import generics
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .filters import FinanceFilter
from rest_framework.response import Response
from django.db import transaction


# Create your views here.
class FinancialList(generics.ListCreateAPIView):
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    queryset = Financial.objects.all()
    serializer_class = FinancialSerializer
    # pagination_class = StandardResultsSetPagination
    filter_class = FinanceFilter

    @transaction.atomic()
    def post(self, request: list):
        out = []
        for i in request.data:
            if "country" in i:
                country = data.pop("country")
            serializer = StockSerializer(data=i)
            if serializer.is_valid():
                stock = serializer.save()

                fin_obj = self.queryset.filter(stock__ticket=i["ticket"])
                if len(fin_obj) == 0:
                    obj = self.queryset.create(stock=stock, country=country)
                else:
                    obj = fin_obj.last()
                    obj.stock = stock
                    obj.country = country
                    obj.save()
                fin_serializer = self.serializer_class(obj)
                out.append(fin_serializer.data)
            else:
                return Response(serializer.errors, status=404)
        return Response(out)

    def put(self, request):
        out = []
        for i in request.data:
            stock = Stock.objects.get(ticket=i["ticket"])
            serializer = StockSerializer(stock, data=i)
            if serializer.is_valid():
                stock = serializer.save()
                try:
                    financial = Financial.objects.get(stock=serializer.data)
                    fin_serializer = self.serializer_class(financial, Fstock=serializer)
                except Exception as e:
                    print(e)
                    fin_data = {"stock": stock.pk}
                    fin_serializer = self.serializer_class(data=fin_data)
                if fin_serializer.is_valid():
                    fin_serializer.save()
                    out.append(fin_serializer.data)
                else:
                    return Response(fin_serializer.errors, status=404)
            else:
                return Response(serializer.errors, status=404)
        return Response(out)


class StocklList(generics.ListCreateAPIView):
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    queryset = Stock.objects.all()
    serializer_class = FinancialSerializer
    # pagination_class = StandardResultsSetPagination
    filter_class = FinanceFilter

    def get(self, request: list):
        out = []
        serializer = StockSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request: list):
        out = []
        for i in request.data:
            if "country" in i:
                country = data.pop("country")
            serializer = StockSerializer(data=i)
            if serializer.is_valid():
                stock = serializer.save()
                return Response(serializer.data, status=404)
        return Response(out)

    def put(self, request):
        out = []
        for i in request.data:
            stock = Stock.objects.get(ticket=i["ticket"])
            serializer = StockSerializer(stock, data=i)
            if serializer.is_valid():
                stock = serializer.save()
                return Response(serializer.data, status=404)
            else:
                return Response(serializer.errors, status=404)
        return Response(out)
