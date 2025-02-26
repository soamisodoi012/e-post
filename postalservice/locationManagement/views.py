from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Address
from .modelSerializer import AdressSerializer
@api_view(['POST'])
def createAdress(request):
    if request.method=='POST':
        serializer=AdressSerializer(data=request.data)
        