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
import math
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Radius of the Earth in miles
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c
@api_view(['POST'])
def add_to_shiping(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            customer = data.get("customer")
            item = data.get("item")
            shipping_cost = data.get("shipping_cost")  # Cost for this item

            # Retrieve locations
            loc1 = get_object_or_404(Address, addresId=data["location1"])
            loc2 = get_object_or_404(Address, addresId=data["location2"])

            # Calculate distance between loc1 and loc2
            distance = haversine(loc1.latitude, loc1.longitude, loc2.latitude, loc2.longitude)

            # Retrieve or create cart in session
            cart = request.session.get('shipping_cart', {})
            if 'items' not in cart:
                cart['items'] = []

            # Append item details to the cart with only serializable data
            cart['customer'] = customer
            cart['items'].append({
                "item": item,
                "location1": loc1.addresId,  # Store only the identifier
                "location2": loc2.addresId,
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

def analyze_description_with_gpt(description):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that detects prohibited items in shipment descriptions."},
                {"role": "user", "content": f"Analyze the following shipment description and respond with 'Yes' if it contains prohibited items, otherwise respond with 'No': {description}"}
            ],
            temperature=0.2
        )
        result = response['choices'][0]['message']['content']
        return result.strip()
    except Exception as e:
        print(f"Error in GPT analysis: {e}")
        return f"Error analyzing description: {str(e)}"
@api_view(['POST'])
def process_order_ship(request):
    if request.method == "POST":
        try:
            print(os.getenv("OPENAI_API_KEY"))  # Debugging to check API key availability

            data = json.loads(request.body)
            customer = get_object_or_404(Customer, username=data.get("customer"))
            description=data.get("description")
            items = data.get("item")
            if not items:
                return JsonResponse({"status": "error", "message": "Missing items in the order"}, status=400)

            for item_data in items:
                # Directly using item_name instead of ForeignKey to Item
                item = item_data.get("item")
                gpt_analysis = analyze_description_with_gpt(description)

                if gpt_analysis.lower() == "yes":
                    return JsonResponse({
                        "status": "error",
                        "message": f"Prohibited item detected: {item}. Reason: {gpt_analysis}"
                    }, status=400)

                loc1 = get_object_or_404(Address, addresId=item_data["location1"])
                loc2 = get_object_or_404(Address, addresId=item_data["location2"])
                distance = haversine(loc1.latitude, loc1.longitude, loc2.latitude, loc2.longitude)

                # Calculate the shipping cost based on distance
                shipping_cost = distance * 0.5  # Assuming the cost is $0.5 per km

                # Generate a unique shipId for each order
                ship_id = f"{customer.username}-{random.randint(100000, 999999)}"

                # Create the ShippingOrder
                ShippingOrder.objects.create(
                    customer=customer,
                    item=item,  # Store the item name directly
                    location1=loc1,
                    location2=loc2,
                    shipping_cost=shipping_cost,  # Use the calculated shipping cost
                    distance=distance,  # Store the calculated distance
                    shipId=ship_id  # Use the generated unique shipId
                )

            return JsonResponse({"status": "success", "message": "Orders placed successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except ValueError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
@api_view(['GET'])
def review_order(request):
    if request.method=='GET':
        orderId=request.GET.get('shipId')
    if orderId:
         queryset = ShippingOrder.objects.filter(shipId=orderId)
         data=ShippingOrderSerilizer(queryset,many=True)
         #serialized_data = list(queryset.values())
         return HttpResponse(data.data)
    else:
         return HttpResponse("Parameter 'param_name' is missing in the request.")
@api_view(['GET'])
def review(request):
    if request.method == 'GET':
        orderId = request.GET.get('shipId')

        if orderId:
            order = get_object_or_404(ShippingOrder, shipId=orderId)

            # Update the status to 'reviewed' or any other status based on your logic
            order.status = 'reviewed'

            # Save the updated status to the database
            order.save()

            return JsonResponse({"status": "success", "message": "Order reviewed successfully", "order_status": order.status})

        else:
            return JsonResponse({"status": "error", "message": "Missing shipId parameter"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method. Only GET is allowed."}, status=405)