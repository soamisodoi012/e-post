from rest_framework import serializers

from .models import Category,Item

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('catCode','catName')
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('itemCode','itemName','catName')