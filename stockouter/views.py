from django.shortcuts import render
from .models import *
from .serializers import StockSerializer,FinancialSerializer,SomeSerializer
from rest_framework import generics
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from .filters import FinanceFilter
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class FinancialList(generics.ListCreateAPIView):
    parser_classes = [FormParser,MultiPartParser,JSONParser]
    queryset = Financial.objects.all()
    serializer_class = FinancialSerializer
    #pagination_class = StandardResultsSetPagination
    filter_class = FinanceFilter
    def post(self,request:list):
        out=[]
        for i in request.data:
            serializer=StockSerializer(data=i)
            if serializer.is_valid():
                serializer.save()
                fin_serializer=self.serializer_class(stock=serializer)
                if fin_serializer.is_valid():
                    fin_serializer.save()
                    out.append(fin_serializer.data)
                else:
                    return Response(serializer.errors,status=404)
            else:
                return Response(serializer.errors,status=404)
        return Response(out)
    def put(self,request):
        out=[]
        for i in request.data:
            stock=Stock.objects.get(ticket=i['ticket'])
            serializer=StockSerializer(stock,data=i)
            if serializer.is_valid():
                stock=serializer.save()
                try:
                    financial=Financial.objects.get(stock=serializer.data)
                    fin_serializer=self.serializer_class(financial,Fstock=serializer)
                except Exception as e:
                    print(e)
                    fin_data={"stock":stock.pk}
                    fin_serializer=self.serializer_class(data=fin_data)
                if fin_serializer.is_valid():
                    fin_serializer.save()
                    out.append(fin_serializer.data)
                else:
                    return Response(fin_serializer.errors,status=404)
            else:
                return Response(serializer.errors,status=404)
        return Response(out)

class SomeView(APIView):
    def post(self,request):
        serializer=SomeSerializer(data=request.data)
        if serializer.is_valid():
            stock=serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=404)
