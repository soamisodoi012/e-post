from django.db import models
from goodsAndItems.models import Category, Item
from customer.models import Customer
from locationManagement.models import Address
from django.utils.crypto import get_random_string
class ShippingOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field="username")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    location1 = models.ForeignKey(Address, related_name='location1_set', on_delete=models.CASCADE)
    location2 = models.ForeignKey(Address, related_name='location2_set', on_delete=models.CASCADE)
    distance = models.FloatField()
    shipping_cost = models.FloatField()
    
    # Unique identifier based on customer, location1, and item
    shipId = models.CharField(max_length=255, unique=True, editable=False, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.shipId:
            self.shipId = f"{self.customer.username}-{self.location1.addresId}-{self.item.itemCode}-{get_random_string(6)}"
        super().save(*args, **kwargs)
