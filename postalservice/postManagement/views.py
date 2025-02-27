from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import json
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
    """ Process the order after the payment. """
    if request.method == "POST":
        try:
            data = request.data  # Use DRF's request.data instead of json.loads(request.body)
            print("Received Data:", data)

            # Validate customer
            if "customer" not in data:
                return Response({"status": "error", "message": "Customer email is missing"}, status=400)

            # Fetch customer object using email (username)
            customer = get_object_or_404(Customer, username=data["customer"])  # ✅ Get Customer instance

            # Validate items
            if "items" not in data:
                return Response({"status": "error", "message": "Missing items in the order"}, status=400)

            for item_data in data["items"]:
                if not all(k in item_data for k in ["item_id", "location1_id", "location2_id", "distance", "shipping_cost"]):
                    return Response({"status": "error", "message": "Missing required item fields"}, status=400)

                # Fetch item using itemCode (not id)
                item = get_object_or_404(Item, itemCode=item_data["item_id"])

                # Fetch locations using addresId (not id)
                location1 = get_object_or_404(Address, addresId=item_data["location1_id"])
                location2 = get_object_or_404(Address, addresId=item_data["location2_id"])

                print("item",item)
                print("item_data",item_data)
                ShippingOrder.objects.create(
                    customer=customer,  
                    item=item,
                    location1=location1,
                    location2=location2,
                    distance=item_data["distance"],
                    shipping_cost=item_data["shipping_cost"]
                )

            return Response({"status": "success", "message": "Order placed successfully"}, status=201)

        except ValueError as e:
            return Response({"status": "error", "message": str(e)}, status=400)

    return Response({"status": "error", "message": "Invalid request method"}, status=405)