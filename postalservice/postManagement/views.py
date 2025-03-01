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
import random
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

            # Retrieve customer using email from the top-level key
            customer = get_object_or_404(Customer, username=data["customer"])
            print("Customer:", customer)

            # Validate required fields
            if "item" not in data or not data["item"]:
                return JsonResponse({"status": "error", "message": "Missing items in the order"}, status=400)

            total_distance = 0
            total_shipping_cost = 0
            
            # Initialize variables for locations and items
            location1 = None
            location2 = None
            order_items = []

            # Loop through items in the order to retrieve details
            for item_data in data["item"]:
                print("Item Data:", item_data)  # Print item data for debugging

                # Retrieve the item
                item = get_object_or_404(Item, itemCode=item_data["item"])

                # Retrieve locations for the item
                loc1 = get_object_or_404(Address, addresId=item_data["location1"])
                loc2 = get_object_or_404(Address, addresId=item_data["location2"])

                # Update total distance and shipping cost
                total_distance += item_data["distance"]
                total_shipping_cost += item_data["shipping_cost"]

                # Set locations (assuming all items have the same locations)
                location1 = loc1
                location2 = loc2

                # Collect items for later use
                order_items.append(item)

            # Create the ShippingOrder instance with total values and locations
            order = ShippingOrder.objects.create(
                customer=customer,
                shipId=f"{customer.username}-{random.randint(100000, 999999)}",  # Generate a unique shipId
                distance=total_distance,
                shipping_cost=total_shipping_cost,
                location1=location1,
                location2=location2
            )

            # Add items to the order
            for item in order_items:
                order.item.add(item)

            order.save()  # Save the order after all items are added

            return JsonResponse({"status": "success", "message": "Order placed successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except ValueError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)