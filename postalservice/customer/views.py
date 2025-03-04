from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Customer
from .modelSerializer import CustomerSerializer
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#from .modelSerializer import CustomerSerializer

@api_view(['POST'])
def createCustomer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()  # Save the customer instance
            return Response(
                {"message": "Customer created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
def updateCustomer(request):
    username = request.GET.get('username')

    if not username:
        return JsonResponse({"status": "error", "message": "Parameter 'username' is missing in the request."}, status=400)

    try:
        customer = Customer.objects.get(username=username)
    except Customer.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Customer not found."}, status=404)

    # Parse request body (expecting JSON)
    try:
        data = json.loads(request.body)  # Load JSON data from request
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)

    # Validate and update customer details
    serializer = CustomerSerializer(customer, data=data, partial=True)  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"status": "success", "message": "Customer updated successfully", "data": serializer.data}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid data", "errors": serializer.errors}, status=400)
@api_view(['GET'])
def getById(request):
    username=request.GET.get("username")
    if not username:
          return JsonResponse({"status": "error", "message": "Parameter 'username' is missing in the request."}, status=400)
    queryset = Customer.objects.filter(username=username)
    data=CustomerSerializer(queryset,many=True)
    serialized_data = list(queryset.values())
    return HttpResponse(data.data)
