from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Category,Item
from rest_framework import status
from .modelSerializer import CatSerializer,ItemSerializer
@api_view(['POST'])
def createCategory(request):
     if request.method == 'POST':
        serializer = CatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert successful", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     else: 
         return HttpResponse("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['GET'])
def getCatById(request):
    param_value = request.GET.get('catCode')
    if param_value:
         queryset = Category.objects.filter(catCode=param_value)
         data=CatSerializer(queryset,many=True)
         #serialized_data = list(queryset.values())
         return HttpResponse(data.data)
    else:
         return HttpResponse("Parameter 'param_name' is missing in the request.")
@api_view(['POST']) 
def createItem(request):
 if request.method=='POST':
  serializer=ItemSerializer(data=request.data)
  if serializer.is_valid():
      serializer.save()
      return  Response("Insert successful", status=status.HTTP_201_CREATED)
@api_view(['GET'])
def getItemById(request):
    param_value = request.GET.get('itemCode')
    if param_value:
         queryset = Category.objects.filter(itemCode=param_value)
         data=ItemSerializer(queryset,many=True)
         #serialized_data = list(queryset.values())
         return HttpResponse(data.data)
    else:
         return HttpResponse("Parameter 'param_name' is missing in the request.")
@api_view(['DELETE'])
def deleteCategory(request):
    catCode = request.GET.get('catCode')

    if not catCode:
        return JsonResponse({"status": "error", "message": "Parameter 'catCode' is missing."}, status=400)

    try:
        category = Category.objects.get(catCode=catCode)
        category.delete()
        return JsonResponse({"status": "success", "message": "Category deleted successfully."}, status=200)
    except Category.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Category not found."}, status=404)
@api_view(['DELETE'])
def deleteItem(request):
    itemCode = request.GET.get('itemCode')

    if not itemCode:
        return JsonResponse({"status": "error", "message": "Parameter 'itemCode' is missing."}, status=400)

    try:
        category = Category.objects.get(itemCode=itemCode)
        category.delete()
        return JsonResponse({"status": "success", "message": "item deleted successfully."}, status=200)
    except Category.DoesNotExist:
        return JsonResponse({"status": "error", "message": "item not found."}, status=404)