from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import json
from .modelSerializer import ShippingOrderSerilizer
from .models import ShippingOrder, Customer, Item, Address
@api_view(['POST'])
def add_to_shiping(request):
    if request.method == "POST":
         if request.method == "POST":
          try:
            data = json.loads(request.body)
            customer = data.get("customer")
            item = data.get("item")
            location1 = data.get("location1")
            location2 = data.get("location2")
            distance = data.get("distance")
            shipping_cost = data.get("shipping_cost")  # Cost for this item
            # Retrieve or create cart in session
            cart = request.session.get('shipping_cart', {})
            if 'items' not in cart:
                cart['items'] = []

            cart['customer'] = customer
            cart['items'].append({
                "item": item,
                "location1": location1,
                "location2": location2,
                "distance": distance,
                "shipping_cost": shipping_cost
            })

            # Calculate the new total shipping cost
            total_shipping_cost = sum(item["shipping_cost"] for item in cart["items"])
            cart["total_shipping_cost"] = total_shipping_cost  # Store in session

            # Save updated cart back to session
            request.session['shipping_cart'] = cart
            request.session.modified = True

            return JsonResponse({
                "status": "success",
                "message": "Item added to cart",
                "cart": cart
            })

          except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@api_view(['POST'])
def remove_from_shiing_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item = data.get("item")

            cart = request.session.get('shipping_cart', {})
            if 'items' in cart:
                cart['items'] = [item for item in cart['items'] if item["item"] != item]

            # Recalculate total shipping cost
            total_shipping_cost = sum(item["shipping_cost"] for item in cart["items"])
            cart["total_shipping_cost"] = total_shipping_cost  # Update session

            request.session['shipping_cart'] = cart
            request.session.modified = True

            return JsonResponse({
                "status": "success",
                "message": "Item removed",
                "cart": cart
            })

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
@api_view(['GET'])
def view_cart(request):
    if request.method == "GET":
     cart = request.session.get('shipping_cart', {"items": [], "total_shipping_cost": 0})
    return JsonResponse({"status": "success", "cart": cart})
@api_view(['POST'])
def process_order_ship(request):
    """Process the order after the payment."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)

            # Retrieve customer using email
            if "customer" in data:
                customer = get_object_or_404(Customer, username=data["customer"])  # Use email (username) to fetch the customer
            else:
                return JsonResponse({"status": "error", "message": "Customer email is missing"}, status=400)

            # Validate required fields
            if "items" not in data:
                return JsonResponse({"status": "error", "message": "Missing items in the order"}, status=400)

            # Loop through items in the order and process
            for item_data in data["items"]:
                item = get_object_or_404(Item, itemCode=item_data["item_id"])  # Use itemCode instead of id
                location1 = get_object_or_404(Address, addresId=item_data["location1"])  # Use addresId instead of id
                location2 = get_object_or_404(Address, addresId=item_data["location2"])  # Use addresId instead of id

                # Create ShippingOrder model entry
                shipId = f"{customer}-{location1}" 
                order = ShippingOrder.objects.create(
                    customer=customer,
                    item=item,
                    location1=location1,
                    location2=location2,
                    shipId=shipId,
                    distance=item_data["distance"],
                    shipping_cost=item_data["shipping_cost"]
                )

            return JsonResponse({"status": "success", "message": "Order placed successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except ValueError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
@api_view(['GET'])
def view_order(request):
 param_value = request.GET.get('shipId')
 print(param_value)  # Useful for debugging

 if param_value:
        # Fetch the specific ShippingOrder instance
        try:
            order = ShippingOrder.objects.get(shipId=param_value)
            # Serialize the order
            serializer = ShippingOrderSerilizer(order)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except ShippingOrder.DoesNotExist:
            return JsonResponse({"error": "ShippingOrder not found."}, status=status.HTTP_404_NOT_FOUND)
 else:
        return JsonResponse({"error": "Parameter 'shipId' is missing in the request."}, status=status.HTTP_400_BAD_REQUEST)