from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
import requests
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework import status, permissions, exceptions
from django.contrib.auth import authenticate
import random
from django.contrib.auth.models import User


# Create your views here.
class Authorization(APIView):
    def post(self,request):
        service =request.data
        try:
            user = authenticate(username=service['username'], password=service['password'])#метод аутентификации,если юзера нет,то выведет None
        except:
            raise exceptions.ValidationError()
        if user is None:
            msg="invalid login or password"
            raise exceptions.AuthenticationFailed(msg)
        return Response({'token':user.token})
class Registration(viewsets.ViewSet):
    def post(self,request):
        try:
            u=User.create_user(username=request.data['username'],password=request.data['password'])
        except Exceptions as e:
            return Response({"error:"e},status=404)
        return Response()
