from rest_framework import serializers
from .models import ShippingOrder
class ShippingOrderSerilizer(serializers.ModelSerializer):
    class Meta:
        model=ShippingOrder
        fields=('customer','item' ,'shipId','location1' ,'location2','distance','shipping_cost','status','description')