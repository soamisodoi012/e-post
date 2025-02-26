from rest_framework import serializers
from .models import Address
class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=('addresId','addresName','distance')