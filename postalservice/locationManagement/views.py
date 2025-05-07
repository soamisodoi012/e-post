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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else: 
         return HttpResponse("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['GET'])
def getAddress(request):
    addresId=request.GET.get('addresId')
    print(addresId)
    if not addresId:
         return JsonResponse({"status": "error", "message": "Parameter 'addresId' is missing in the request."}, status=400)
    queryset = Address.objects.filter(addresId=addresId)
    data=AdressSerializer(queryset,many=True)
    serialized_data = list(queryset.values())
    return HttpResponse(data.data)