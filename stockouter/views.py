from django.shortcuts import render
from .models import *
from .serializers import StockSerializer,FinancialSerializer
from rest_framework import generics
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from .filters import FinanceFilter
from rest_framework.response import Response


# Create your views here.
class FinancialList(generics.ListCreateAPIView):
    parser_classes = [FormParser,MultiPartParser,JSONParser]
    queryset = Financial.objects.all()
    serializer_class = FinancialSerializer
    #pagination_class = StandardResultsSetPagination
    filter_class = FinanceFilter
