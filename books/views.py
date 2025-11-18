from django.shortcuts import render
from django.http import HttpResponse  # <-- import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models as book_model
from . import serializers as book_serializer

class BookListAPI(APIView):
    def get(self,request):
        pass

def hello_world(request):
    return HttpResponse('hello world')