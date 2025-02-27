from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Customer
from .modelSerializer import CustomerSerializer
@api_view(['POST'])
def createCustomer(request):
    if request.method=='POST':
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(" successful", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else: 
         return HttpResponse("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)